from transformer import Transformer

from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser(description="Transforms the kselftest files.")
    parser.add_argument("path", type=str, help="The path to the kselftest directory.")
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="If set, the files will be transformed in place.",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        help="The file to write the transformed content to.",
    )
    args = parser.parse_args()

    transformer = Transformer()
    transformer.transform(args.path, args.in_place, args.output_file)
