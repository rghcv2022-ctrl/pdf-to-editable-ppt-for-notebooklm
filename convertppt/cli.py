import argparse
import os

from .core import build_output_path, convert_file, log_runtime_summary


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert PDF or image-based PowerPoint files to editable PPTX."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="test.pptx",
        help="Input file path (.pdf/.ppt/.pptx). Defaults to test.pptx.",
    )
    parser.add_argument(
        "output",
        nargs="?",
        help="Optional output PPTX path. Defaults to <input>_AI_REPAIRED.pptx.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_file = args.input
    output_file = args.output or build_output_path(input_file)

    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        return 1

    try:
        log_runtime_summary(print)
        convert_file(input_file, output_file, logger=print)
    except Exception as exc:
        print(f"Conversion failed: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
