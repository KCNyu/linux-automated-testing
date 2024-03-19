import os

class CodePreprocessor:
    def __init__(self, filename, output_filename=None):
        self.filename = filename
        self.output_filename = output_filename if output_filename else filename

    def __write_lines(self, lines):
        with open(self.output_filename, "w") as file:
            file.writelines(lines)

    def __add_braces_to_ifs(self):
        with open(self.filename, "r") as file:
            lines = file.readlines()

        new_lines = []
        skip_next_line = False
        for i, line in enumerate(lines):
            if skip_next_line:
                skip_next_line = False
                continue

            if "if" in line and not line.strip().endswith("}") and "{" not in line and "#" not in line:
                indent = len(line) - len(line.lstrip())
                next_line_index = i + 1 if i + 1 < len(lines) else i
                next_line_indent = len(lines[next_line_index]) - len(
                    lines[next_line_index].lstrip()
                )

                if next_line_indent > indent and "{" not in lines[next_line_index]:
                    new_line = line.rstrip() + " {\n"
                    next_line = (
                        lines[next_line_index].rstrip() + "\n" + " " * indent + "}\n"
                    )
                    new_lines.append(new_line)
                    new_lines.append(next_line)
                    skip_next_line = True
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        self.__write_lines(new_lines)

    def __update_cocci_include_path(self, kselftest_harness_path: str):
        relative_path = os.path.relpath(
            kselftest_harness_path, start=os.path.dirname(self.filename)
        )
        new_include_directive = f'#include "{relative_path}"'

        with open(self.filename, "r") as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            if '"PATH/kselftest_harness.h"' in line:
                line = line.replace(
                    '#include "PATH/kselftest_harness.h"', new_include_directive
                )
            new_lines.append(line)

        self.__write_lines(new_lines)

    @staticmethod
    def add_braces(filename: str, in_place: bool = True, output_filename: str = None):
        if not in_place:
            output_filename = (
                output_filename if output_filename else filename + "_transformed"
            )
        processor = CodePreprocessor(filename, output_filename)
        processor.__add_braces_to_ifs()
        print(f"Processed {filename}.")

    @staticmethod
    def reset_kselftest_path(
        filename: str,
        kselftest_harness_path: str,
        in_place: bool = True,
        output_filename: str = None,
    ):
        if not in_place:
            output_filename = (
                output_filename if output_filename else filename + "_transformed"
            )
        processor = CodePreprocessor(filename, output_filename)
        processor.__update_cocci_include_path(kselftest_harness_path)
        print(f"Processed {filename} with updated kselftest_harness path.")
