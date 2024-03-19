import subprocess
import os


class CoccinelleRunner:
    def __init__(self, cocci_file):
        self.cocci_file = cocci_file

    def run_transformation(self, source_file, in_place=True, output_file=None):
        """
        Runs a Coccinelle transformation on a source file.
        """
        if not in_place and output_file is None:
            output_file = source_file + "_transformed"

        command = ["spatch", "--sp-file", self.cocci_file, source_file]
        if in_place:
            # insert before the source_file
            command.insert(3, "--in-place")
        else:
            command.extend(["-o", output_file])

        devnull = open(os.devnull, "w")
        try:
            subprocess.run(command, check=True, stdout=devnull, stderr=devnull)
            print(
                f"Transformation {'complete' if in_place else 'written to ' + output_file}."
            )
        except subprocess.CalledProcessError as e:
            print(f"Error running Coccinelle: {e}")

    @staticmethod
    def run(path: str, cocci_file: str, in_place=True, output_file=None):
        """
        Runs a Coccinelle transformation on a source file.

        Parameters:
        - path: The path to the source file to transform.
        - cocci_file: The path to the .cocci script to be used for transformation.
        - in_place: If True, modifies the source file in place. Otherwise, writes to output_file.
        - output_file: The path to the output file. Used only if in_place is False. If not provided,
                       defaults to appending '_transformed' to the source file name.
        """
        runner = CoccinelleRunner(cocci_file)
        runner.run_transformation(path, in_place, output_file)
