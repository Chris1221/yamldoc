import yamldoc
import argparse


def cli():
    parser = argparse.ArgumentParser(prog="YAML Documentation Engine")
    parser.add_argument("yaml_path", help="YAML file.")
    parser.add_argument("-c", "--char", default="#'", help="Metadata character prefix.")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Show debug information."
    )
    parser.add_argument(
        "-s",
        "--schema-path",
        default=None,
        help="(Optional) Schema file describing variable types.",
    )
    parser.add_argument(
        "-e",
        "--exclude-char",
        default="#'!",
        help="Prefix to exclude the following entry from generated documentation.",
    )
    parser.add_argument(
        "--override-exclude",
        action="store_true",
        help="Override the exclusion character and force inclusion of all entries.",
    )

    args = parser.parse_args()

    yamldoc.main(**(vars(args)))
