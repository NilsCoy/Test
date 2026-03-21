import argparse
from scripts.pipeline import run_pipeline


def main():
    """Запуск кода из cmd"""
    parser = argparse.ArgumentParser(description="Video translate pipeline")

    parser.add_argument("--input", required=True, help="Video URL or local file")
    parser.add_argument("--output", required=True, help="Output video path")

    # parser.add_argument(
    #     "--downloader",
    #     choices=["yt_dlp", "playwright"],
    #     default="playwright",
    #     help="Download method",
    # )

    parser.add_argument(
        "--translator",
        choices=["v1", "v2"],
        default="v1",
        help="Translate version",
    )

    args = parser.parse_args()

    run_pipeline(
        input_path=args.input,
        output_path=args.output,
        #downloader=args.downloader,
        translator=args.translator,
    )


if __name__ == "__main__":
    main()