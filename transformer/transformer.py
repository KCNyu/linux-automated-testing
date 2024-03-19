import shutil
from code_preprocessor import CodePreprocessor
from coccinelle_runner import CoccinelleRunner
import os


class TransformerFilePath:
    def __init__(self):
        self.coccinelle_kselftest_header_path = "./kselftest/0_kselftest_header.cocci"
        self.coccinelle_kselftest_main_path = "./kselftest/1_kselftest_main.cocci"
        self.coccinelle_kselftest_print_path = "./kselftest/2_kselftest_print.cocci"
        self.coccinelle_kselftest_if_path = "./kselftest/3_kselftest_if.cocci"
        self.coccinelle_kselftest_metadata_path = (
            "./kselftest/4_kselftest_metadata.cocci"
        )

        self.kseltest_harness_path = "../api/kselftest_harness.h"


class Transformer:
    def __init__(self):
        """Initializes the Transformer."""
        self.file_path = TransformerFilePath()

    def __update_test_main(
        self, file_path: str, in_place=True, output_file=None
    ) -> None:
        with open(file_path, "r") as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            if line.strip().startswith("// TEST_HARNESS_MAIN"):
                new_lines.append(line[3:])
            elif line.strip().startswith("TEST("):
                new_lines.append(line.replace("TEST(", "TEST(main_test"))
            else:
                new_lines.append(line)

        if in_place:
            with open(file_path, "w") as file:
                file.writelines(new_lines)
        else:
            with open(output_file, "w") as file:
                file.writelines(new_lines)

    def __update_assert_expression(
        self, file_path: str, in_place=True, output_file=None
    ) -> None:
        with open(file_path, "r") as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            if line.strip().find("ASSERT_") != -1 and line.strip().find("; {") != -1:
                new_lines.append(line.replace("; {", " {"))
            else:
                new_lines.append(line)

        if in_place:
            with open(file_path, "w") as file:
                file.writelines(new_lines)
        else:
            with open(output_file, "w") as file:
                file.writelines(new_lines)

    @staticmethod
    def transform(path: str, in_place=True, output_file=None) -> None:
        transformer = Transformer()
        bak_file = path + ".bak"
        os.system(f"cp {path} {bak_file}")

        if not in_place:
            output_file = path.split(".c")[0] + "_transformed.c"

        # step 1: add braces to if statements and reset kselftest path
        # CodePreprocessor.add_braces(path)
        CodePreprocessor.reset_kselftest_path(
            path, transformer.file_path.coccinelle_kselftest_header_path
        )

        # step 2: run coccinelle to make sure the kselftest.h is included and add it if not
        CoccinelleRunner.run(
            path, transformer.file_path.coccinelle_kselftest_header_path
        )

        # step 3: run coccinelle to add the main test function
        CoccinelleRunner.run(path, transformer.file_path.coccinelle_kselftest_main_path)
        transformer.__update_test_main(path)

        # step 4: run coccinelle to replace the print function
        CoccinelleRunner.run(
            path, transformer.file_path.coccinelle_kselftest_print_path
        )

        # step 5: run coccinelle to update the if statements
        CoccinelleRunner.run(path, transformer.file_path.coccinelle_kselftest_if_path)
        transformer.__update_assert_expression(path)

        # step 6: run coccinelle to add the metadata
        CoccinelleRunner.run(
            path, transformer.file_path.coccinelle_kselftest_metadata_path
        )

        if not in_place:
            os.system(f"mv {path} {output_file}")
            os.system(f"mv {bak_file} {path}")
            os.system(f"diff {path} {output_file}")
        else:
            os.system(f"diff {path} {bak_file}")
            os.system(f"rm {bak_file}")
