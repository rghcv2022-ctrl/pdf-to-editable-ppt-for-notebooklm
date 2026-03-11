import os

from converter_core import convert_file, log_runtime_summary


def main() -> int:
    input_file = "test.pdf"
    output_file = "final_clean_kmeans.pptx"

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
