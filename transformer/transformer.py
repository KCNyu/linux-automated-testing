import subprocess
import argparse
import os
from typing import List


class Transformer:
    """
    A class to transform C test files using Semantic Patch Language (SmPL) through Coccinelle.

    Methods:
    - run_cocci: Executes the Coccinelle transformation on a single file.
    - update_test_main: Modifies the main test harness declaration in a file's content.
    - update_assert_expression: Adjusts ASSERT_ expressions for compatibility.
    - insert_header: Ensures the inclusion of the kselftest_harness.h header.
    - transform: Applies a sequence of transformations to a single file.
    - process_directory: Processes multiple files in a directory, applying transformations.
    """

    def __init__(self):
        """Initializes the Transformer."""
        pass

    def run_cocci(
        self, input_test_file: str, output_test_file: str, cocci_file: str
    ) -> None:
        """
        Executes the Coccinelle (spatch) transformation on a single C file.

        Parameters:
        - input_test_file: The path to the input C file.
        - output_test_file: The path where the transformed file will be saved.
        - cocci_file: The path to the .cocci script to be used for transformation.

        Example:
        run_cocci("input.c", "output.c", "transform.cocci")
        """
        subprocess.run(
            [
                "spatch",
                "-sp_file",
                cocci_file,
                input_test_file,
                "-o",
                output_test_file,
            ]
        )

    def update_test_main(self, lines: List[str]) -> List[str]:
        """
        Updates the TEST_HARNESS_MAIN declaration in the given lines of a C file.

        Parameters:
        - lines: A list of strings representing the lines of the file content.

        Returns:
        - A list of strings with the TEST_HARNESS_MAIN declaration uncommented.

        Example:
        lines = update_test_main(lines)
        """
        new_lines = []
        for line in lines:
            if line.strip().startswith("// TEST_HARNESS_MAIN"):
                new_lines.append(line[3:])
            elif line.strip().startswith("TEST("):
                new_lines.append(line.replace("TEST(", "TEST(main_test"))
            else:
                new_lines.append(line)
        return new_lines

    def update_assert_expression(self, lines: List[str]) -> List[str]:
        """
        Updates ASSERT_ expressions in the given lines by removing semicolons before blocks.

        Parameters:
        - lines: A list of strings representing the lines of the file content.

        Returns:
        - A list of strings with updated ASSERT_ expressions.

        Example:
        lines = update_assert_expression(lines)
        """
        new_lines = []
        for line in lines:
            if line.strip().find("ASSERT_") != -1 and line.strip().find("; {") != -1:
                new_lines.append(line.replace("; {", " {"))
            else:
                new_lines.append(line)
        return new_lines

    def update_args(self, lines: List[str]) -> List[str]:
        """
        Update the argc and argv to __global_argc and __global_argv if exists

        Parameters:
        - lines: A list of strings representing the lines of the file content.

        Returns:
        - A list of strings with updated argc and argv.

        """
        new_lines = []
        for line in lines:
            if "argc" in line:
                line = line.replace("argc", "__global_argc")
            if "argv" in line:
                line = line.replace("argv", "__global_argv")
            new_lines.append(line)
        return new_lines

    def insert_header(self, lines: List[str]) -> List[str]:
        """
        Inserts the kselftest_harness.h header into the given lines if not already included.

        Parameters:
        - lines: A list of strings representing the lines of the file content.

        Returns:
        - A list of strings with the header included at the appropriate position.

        Example:
        lines = insert_header(lines)
        """
        new_lines = []
        include = False
        for line in lines:
            if line.strip().startswith("#include"):
                if not include:
                    new_lines.append('#include "include/kselftest_harness.h"\n')
                    include = True
            new_lines.append(line)
        return new_lines

    def transform(
        self, input_test_file: str, output_test_file: str, cocci_file: str
    ) -> None:
        """
        Transforms a C file by applying a series of updates for test harness compatibility.

        Parameters:
        - input_test_file: Path to the input C file.
        - output_test_file: Path where the transformed file will be saved.
        - cocci_file: Path to the .cocci script used for initial transformation.

        Example:
        transform("input.c", "output.c", "transform.cocci")
        """

        self.run_cocci(input_test_file, output_test_file, cocci_file)

        # if do not exists file for output then create it at first
        if not os.path.exists(output_test_file):
            with open(output_test_file, "w") as file:
                file.write("")
        with open(output_test_file, "r") as file:
            lines = file.readlines()

        lines = self.update_test_main(lines)
        lines = self.update_assert_expression(lines)
        lines = self.update_args(lines)
        lines = self.insert_header(lines)

        with open(output_test_file, "w") as file:
            file.writelines(lines)

    def process_directory(self, directory: str, cocci_file: str) -> None:
        """
        Processes all C files in a given directory, applying transformation if they don't already include
        specific headers. This method is useful for batch processing, automating the transformation of
        multiple files in a directory structure.

        Parameters:
        - directory: The path to the directory containing C files to be processed.
        - cocci_file: The path to the .cocci script used for the transformation.
        """

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".c"):
                    file_path = os.path.join(root, file)
                    if file_path.endswith("_transformed.c"):
                        continue
                    with open(file_path, "r") as f:
                        if (
                            "kselftest.h" not in f.read()
                            and "kselftest_harness.h" not in f.read()
                        ):
                            output_file_path = file_path.replace(".c", "_transformed.c")
                            self.transform(file_path, output_file_path, cocci_file)
                            print(f"Transformed: {file_path} -> {output_file_path}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transform a test file or all .c files in a directory using a .cocci file."
    )
    parser.add_argument(
        "-i", "--input", help="Input test file or directory", required=True
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output test file or directory for transformed files",
        required=False,
    )
    parser.add_argument("-s", "--spatch", help="Spatch file .cocci", required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    transformer = Transformer()

    if os.path.isdir(args.input):
        if args.output and not os.path.isdir(args.output):
            print(f"Output path {args.output} is not a directory.")
        else:
            transformer.process_directory(args.input, args.spatch)
    else:
        if args.output is None:
            args.output = args.input.replace(".c", "_transformed.c")
            transformer.transform(args.input, args.output, args.spatch)
        else:
            transformer.transform(args.input, args.output, args.spatch)
