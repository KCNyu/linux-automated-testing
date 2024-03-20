import os
import re


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
        i = 0
        while i < len(lines):
            # Check for 'if' and 'else' statements that are not followed by an opening brace
            if re.match(r"\s*if\s*\(.*\)\s*$", lines[i]) or re.match(
                r"\s*else\s*(if\s*\(.*\))?\s*$", lines[i]
            ):
                control_structure = "if" if "if" in lines[i] else "else"
                # Insert an opening brace at the end of the 'if' or 'else' line if not present
                if not lines[i].strip().endswith("{"):
                    lines[i] += " {"
                # Move forward to find the end of the block
                j = i + 1
                depth = 1  # Keep track of braces to handle nested structures
                while j < len(lines) and depth > 0:
                    line_strip = lines[j].strip()
                    if line_strip.endswith("{"):
                        depth += 1
                    if line_strip.endswith("}"):
                        depth -= 1
                    if depth == 0 or (depth == 1 and line_strip.endswith(";")):
                        # If we find the end of the block or a simple statement, close the block
                        lines[j] += " }"
                        break
                    j += 1
            i += 1

        self.__write_lines(lines)

    def __update_cocci_include_path(self, kselftest_harness_path: str):
        relative_path = os.path.relpath(
            kselftest_harness_path, start=os.path.dirname(self.filename)
        )
        new_include_directive = f'#include "../kselftest_harness.h"'

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
        # print(f"Processed {filename} with updated kselftest_harness path.")
