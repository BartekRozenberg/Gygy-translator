"""Command-line interface for Gygy translator."""

import argparse

from gygy.engine import translate


def main() -> None:
    parser = argparse.ArgumentParser(description="Gygy translator CLI")
    parser.add_argument("text", nargs="?", default="", help="Text to translate")
    args = parser.parse_args()
    print(translate(args.text))


if __name__ == "__main__":
    main()
