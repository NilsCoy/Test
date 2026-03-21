import os
from scripts.download_utils import yt_dlp_download, playwright_download
from scripts.translate_utils import translate_v1, translate_v2


def is_url(path: str) -> bool:
    """Проверка на ссылку"""
    return path.startswith("http://") or path.startswith("https://")


def run_pipeline(
    input_path: str,
    output_path: str,
    downloader: str = "yt_dlp",
    translator: str = "v2",
):
    """Запуск полного цикла перевода"""
    print(f"\nStart: {input_path}")

    # 1. Определяем источник
    if is_url(input_path):
        print("Input detected as URL")

        # if downloader == "yt_dlp":
        #     video_path = yt_dlp_download(input_path)
        # elif downloader == "playwright":
        #     video_path = playwright_download(input_path)
        # else:
        #     raise ValueError("Unknown downloader")

        try:
            video_path = yt_dlp_download(input_path)
        except:
            try:
                video_path = playwright_download(input_path)
            except:
                raise ValueError("Unknown downloader")

    else:
        print("Input detected as local file")

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"File not found: {input_path}")

        video_path = input_path

    print(f"Using video: {video_path}")

    # 2. Translate
    if translator == "v1":
        result = translate_v1(video_path, output_path)
    elif translator == "v2":
        result = translate_v2(video_path, output_path)
    else:
        raise ValueError("Unknown translator")

    print(f"Done: {result}")
    return result