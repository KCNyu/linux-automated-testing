from preprocessor import CodePreprocessor
from runner import CoccinelleRunner
from tqdm import tqdm
import os
import signal


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

    def __update_metadata(
        self, file_path: str, in_place=True, output_file=None
    ) -> None:
        with open(file_path, "r") as file:
            lines = file.readlines()

        new_lines = []
        main_test = False
        for line in lines:
            if line.strip().startswith("TEST("):
                main_test = True
            if main_test and "argc" in line:
                line = line.replace("argc", "__test_global_metadata->argc")
            if main_test and "argv" in line:
                line = line.replace("argv", "__test_global_metadata->argv")
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
        with open(file_path, "r") as file:
            lines = file.readlines()

        new_lines = []
        under_test = False
        for line in lines:
            if line.strip().find("TEST(") != -1:
                under_test = True
                new_lines.append(line)
            else:
                if line.strip().startswith("printf"):
                    if under_test:
                        line = line.replace("printf", "TH_LOG")
                    else:
                        line = line.replace("printf", "ksft_print_msg")
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
        for line in lines:
            if "exit(0)" in line:
                line = line.replace("exit(0)", "exit(KSFT_PASS)")
            if "exit(1)" in line:
                line = line.replace("exit(1)", "exit(KSFT_FAIL)")
            if "exit(2)" in line:
                line = line.replace("exit(2)", "exit(KSFT_XFAIL)")
            if "exit(3)" in line:
                line = line.replace("exit(3)", "exit(KSFT_XPASS)")
            if "exit(4)" in line:
                line = line.replace("exit(4)", "exit(KSFT_SKIP)")
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
        # CoccinelleRunner.run(
        #     path, self.file_path.coccinelle_kselftest_print_path
        # )
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
        bak_file = path + ".bak"
        os.system(f"cp {path} {bak_file}")

        if not in_place:
            output_file = path.split(".c")[0] + "_transformed.c"

        functions = transformer.transfrom_impl.retun_execution(
            path, in_place, output_file
        )

        signal.signal(signal.SIGALRM, handle_timeout)
        signal.alarm(15)

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
            os.system(f"diff --color=always {path} {output_file}")
        else:
            os.system(f"diff --color=always {bak_file} {path}")
            os.system(f"rm {bak_file}")
