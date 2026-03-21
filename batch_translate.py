import subprocess
from pathlib import Path
import json

# НАСТРОЙКИ
TRANSLATOR = "v1"  # или "v2"
OUTPUT_DIR = Path("outputs")
JSON_FILE = "translate_videos.json"

# ССЫЛКИ
def load_video_urls(json_path: str) -> dict:
    """Загрузка ссылок из JSON"""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_translation(input_url: str, output_file: Path):
    """Запуск перевода одного видео"""
    command = [
        "make",
        "run-url",
        f'INPUT={input_url}',
        f'OUTPUT={output_file}',
        f'TRANSLATOR={TRANSLATOR}',
    ]

    try:
        print(f"Обработка: {input_url}")
        subprocess.run(command, check=True)
        print(f"Готово: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при обработке {input_url}: {e}")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    video_urls = load_video_urls(JSON_FILE)

    for video in video_urls.keys():
        output_file = OUTPUT_DIR / f"video_{video}.mp4"
        run_translation(video_urls[video], output_file)


if __name__ == "__main__":
    main()