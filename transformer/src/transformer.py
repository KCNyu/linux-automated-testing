from preprocessor import CodePreprocessor
from runner import CoccinelleRunner
from tqdm import tqdm
import os
import signal
import re

TIMEOUT = 120


def handle_timeout(signum, frame):
    raise TimeoutError


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


class TransformerIMPL:
    def __init__(self, file_path: TransformerFilePath):
        """Initializes the Transformer."""
        self.file_path = file_path

    def __update_test_main(
        self, file_path: str, in_place=True, output_file=None
    ) -> None:
        with open(file_path, "r") as file:
            lines = file.readlines()

        new_lines = []
        in_test = False
        brace_count = 0
        last_return_index = None  # Keep track of the last "return <expression>;" line within a TEST function

        for i, line in enumerate(lines):
            if line.strip().startswith("// TEST_HARNESS_MAIN"):
                new_lines.append(line[3:])
                continue
            if line.strip().startswith("TEST("):
                new_lines.append(line.replace("TEST(", "TEST(main_test"))
                in_test = True
                continue

            if in_test:
                brace_count += line.count("{")
                brace_count -= line.count("}")

                # Use regular expression to find "return <expression>;"
                if re.search(r"\breturn\s+.*?;", line):
                    last_return_index = len(
                        new_lines
                    )  # Update the index with current line in new_lines

                if brace_count == 0:
                    # Exiting TEST function
                    in_test = False
                    if last_return_index is not None:
                        # Extract the return expression and replace it
                        return_match = re.search(
                            r"\breturn\s+(.*?);", new_lines[last_return_index]
                        )
                        if return_match:
                            return_expression = return_match.group(1)
                            # Replace the last "return <expression>;" with "exit(<expression>);"
                            new_lines[last_return_index] = re.sub(
                                r"\breturn\s+.*?;",
                                f"exit({return_expression});",
                                new_lines[last_return_index],
                            )
                    last_return_index = None  # Reset for the next TEST function
            new_lines.append(line)

        # Write to either the original file or a new output file
        output_path = file_path if in_place else output_file
        with open(output_path, "w") as file:
            file.writelines(new_lines)

    def __update_assert_expression(
        self, file_path: str, in_place=True, output_file=None
    ) -> None:
        with open(file_path, "r") as file:
            lines = file.readlines()

        new_lines = []
        in_test = False
        found = True
        for line in lines:
            if line.strip().startswith("TEST("):
                in_test = True
            if in_test:
                pattern = r'(?<![":\'/])\breturn\b(?![":\'/])'
                replacement = lambda match: re.sub(
                    r"return\s+(.*?);", r"exit(\1);", match.group(0)
                )
                new_line = re.sub(pattern, replacement, line, flags=re.DOTALL)
                if new_line != line:
                    new_lines.append(new_line)
                    continue
            if not found:
                if line.strip().find("; {") != -1:
                    new_lines.append(line.replace("; {", " {"))
                    found = True
                    continue
                elif line.strip().find("; // {") != -1:
                    new_lines.append(line.replace("; // {", " {"))
                    found = True
                    continue
            if line.strip().find("ASSERT_") != -1:
                if line.strip().find("; {") != -1:
                    new_lines.append(line.replace("; {", " {"))
                elif line.strip().find("; // {") != -1:
                    new_lines.append(line.replace("; // {", " {"))
                else:
                    found = False
                    new_lines.append(line)
                    continue
            elif line.strip().startswith("// }"):
                new_lines.append(line.replace("// }", "}"))
            else:
                new_lines.append(line)

        if in_place:
            with open(file_path, "w") as file:
                file.writelines(new_lines)
        else:
            with open(output_file, "w") as file:
                file.writelines(new_lines)

    def __update_metadata(
        self, file_path: str, in_place=True, output_file=None
    ) -> None:
        with open(file_path, "r") as file:
            lines = file.readlines()

        argc_pattern = re.compile(r"\bargc\b")
        argv_pattern = re.compile(r"\bargv\b")

        new_lines = []
        main_test = False
        for line in lines:
            if line.strip().startswith("TEST("):
                main_test = True
            if main_test:
                line = argc_pattern.sub("__test_global_metadata->argc", line)
                line = argv_pattern.sub("__test_global_metadata->argv", line)
            new_lines.append(line)

        if in_place:
            with open(file_path, "w") as file:
                file.writelines(new_lines)
        else:
            with open(output_file, "w") as file:
                file.writelines(new_lines)

    def __update_print_expression(
        self, file_path: str, in_place=True, output_file=None
    ) -> None:
        def replacement(match):
            string_part = match.group(1)
            extra_params = match.group(3)
            if extra_params:
                return f'{replacement_function}("{string_part}", {extra_params});'
            else:
                return f'{replacement_function}("{string_part}");'

        with open(file_path, "r") as file:
            lines = file.readlines()

        new_lines = []
        under_test = False
        regex = r'printf\("((?:[^"\\]|\\.)*?)(\\n)?"(?:,\s*([^;]*))?\);'

        for line in lines:
            if "TEST(" in line.strip():
                under_test = True
            else:
                if line.strip().startswith("printf"):
                    if under_test:
                        replacement_function = "TH_LOG"
                        line = re.sub(regex, replacement, line)
                    else:
                        replacement_function = "ksft_print_msg"
                        line = line.replace("printf", replacement_function)
            new_lines.append(line)

        if in_place:
            with open(file_path, "w") as file:
                file.writelines(new_lines)
        else:
            with open(output_file, "w") as file:
                file.writelines(new_lines)

    def __update_exit_value(
        self, file_path: str, in_place=True, output_file=None
    ) -> None:
        with open(file_path, "r") as file:
            lines = file.readlines()

        new_lines = []
        exit_pattern = re.compile(r"exit\((\d)\)")
        function_pattern = re.compile(r"ksft_exit_(pass|fail|xfail|xpass|skip)\(\)")

        exit_macros = {
            "0": "KSFT_PASS",
            "1": "KSFT_FAIL",
            "2": "KSFT_XFAIL",
            "3": "KSFT_XPASS",
            "4": "KSFT_SKIP",
        }

        function_macros = {
            "pass": "KSFT_PASS",
            "fail": "KSFT_FAIL",
            "xfail": "KSFT_XFAIL",
            "xpass": "KSFT_XPASS",
            "skip": "KSFT_SKIP",
        }

        for line in lines:
            match_exit = exit_pattern.search(line)
            if match_exit:
                exit_code = match_exit.group(1)
                if exit_code in exit_macros:
                    line = exit_pattern.sub(f"exit({exit_macros[exit_code]})", line)
            match_function = function_pattern.search(line)
            if match_function:
                function_key = match_function.group(1)
                if function_key in function_macros:
                    line = function_pattern.sub(
                        f"{function_macros[function_key]}", line
                    )
            new_lines.append(line)

        if in_place:
            with open(file_path, "w") as file:
                file.writelines(new_lines)
        else:
            with open(output_file, "w") as file:
                file.writelines(new_lines)

    def __reset_kselftest_path(
        self, path: str, in_place=True, output_file=None
    ) -> None:
        # CodePreprocessor.add_braces(path)
        CodePreprocessor.reset_kselftest_path(
            path, self.file_path.coccinelle_kselftest_header_path
        )

    def __reset_header_path(self, path: str, in_place=True, output_file=None) -> None:
        CoccinelleRunner.run(path, self.file_path.coccinelle_kselftest_header_path)

    def __reset_test_main(self, path: str, in_place=True, output_file=None) -> None:
        CoccinelleRunner.run(path, self.file_path.coccinelle_kselftest_main_path)
        self.__update_test_main(path)

    def __reset_print_expression(
        self, path: str, in_place=True, output_file=None
    ) -> None:
        CoccinelleRunner.run(path, self.file_path.coccinelle_kselftest_print_path)
        self.__update_print_expression(path)

    def __reset_assert_expression(
        self, path: str, in_place=True, output_file=None
    ) -> None:
        CoccinelleRunner.run(path, self.file_path.coccinelle_kselftest_if_path)
        self.__update_assert_expression(path)

    def __reset_exit_expression(
        self, path: str, in_place=True, output_file=None
    ) -> None:
        self.__update_exit_value(path)

    def __reset_metadata(self, path: str, in_place=True, output_file=None) -> None:
        # CoccinelleRunner.run(
        #     path, self.file_path.coccinelle_kselftest_metadata_path
        # )
        self.__update_metadata(path)

    def retun_execution(self, path: str, in_place=True, output_file=None):
        return [
            # step 1: add braces to if statements and reset kselftest path
            (self.__reset_kselftest_path, (path, in_place, output_file)),
            # step 2: run coccinelle to make sure the kselftest.h is included and add it if not
            (self.__reset_header_path, (path, in_place, output_file)),
            # step 3: run coccinelle to add the main test function
            (self.__reset_test_main, (path, in_place, output_file)),
            (
                # step 4: run coccinelle to replace the print function
                self.__reset_print_expression,
                (path, in_place, output_file),
            ),
            (
                # step 5: run coccinelle to update the if statements
                self.__reset_assert_expression,
                (path, in_place, output_file),
            ),
            # step 6: replace the exit value with actual kselftest exit codes
            (self.__reset_exit_expression, (path, in_place, output_file)),
            # step 7: run coccinelle to add the metadata
            (self.__reset_metadata, (path, in_place, output_file)),
        ]


class Transformer:
    def __init__(self):
        """Initializes the Transformer."""
        self.transfrom_impl = TransformerIMPL(TransformerFilePath())

    @staticmethod
    def transform(path: str, in_place=True, output_file=None) -> None:
        if not path.endswith(".c"):
            return
        transformer = Transformer()
        with open(path, "r") as file:
            lines = file.readlines()
        for line in lines:
            if "#include" in line and "kselftest_harness.h" in line:
                print(f"SKIP: {path} already contains kselftest_harness.h")
                return
        bak_file = path + ".bak"
        os.system(f"cp {path} {bak_file}")

        if not in_place:
            output_file = path.split(".c")[0] + "_transformed.c"

        functions = transformer.transfrom_impl.retun_execution(
            path, in_place, output_file
        )

        signal.signal(signal.SIGALRM, handle_timeout)
        signal.alarm(TIMEOUT)

        try:
            functions = transformer.transfrom_impl.retun_execution(
                path, in_place, output_file
            )
            desc = "Transforming " + path.split("/")[-1]
            for function, args in tqdm(functions, desc=desc):
                function(*args)
            signal.alarm(0)
        except TimeoutError:
            print("Transforme Failed!")
            os.system(f"mv {bak_file} {path}")
            return

        if not in_place:
            os.system(f"mv {path} {output_file}")
            os.system(f"mv {bak_file} {path}")
            os.system(f"diff -u --color=always {path} {output_file}")
        else:
            os.system(f"diff -u --color=always {bak_file} {path}")
            os.system(f"rm {bak_file}")

        os.system(f"rm {path}.ast_raw >/dev/null 2>&1")
        os.system(f"rm {path}.depend_raw >/dev/null 2>&1")
