import subprocess
from pathlib import Path
import json
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Batch video translator")

    parser.add_argument(
        "--json",
        default="exampl_videos.json",
        help="Путь к JSON файлу со ссылками",
    )

    parser.add_argument(
        "--translator",
        default="v1",
        choices=["v1", "v2"],
        help="Тип переводчика",
    )

    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Папка для сохранения видео",
    )

    return parser.parse_args()


def load_video_urls(json_path: str) -> dict:
    """Загрузка ссылок из JSON"""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Невалидный JSON: {e}")
        exit(1)
    except FileNotFoundError:
        print(f"[ERROR] Файл не найден: {json_path}")
        exit(1)

def run_translation(input_url: str, output_file: Path, translator: str):
    """Запуск перевода одного видео"""
    command = [
        "make",
        "translate",
        f"INPUT={input_url}",
        f"OUTPUT={output_file}",
        f"TRANSLATOR={translator}",
    ]

    try:
        print(f"[INFO] Обработка: {input_url}")
        subprocess.run(command, check=True)
        print(f"[SUCCESS] Готово: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Ошибка при обработке {input_url}: {e}")


def main():
    args = parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    video_urls = load_video_urls(args.json)

    for name, url in video_urls.items():
        output_file = output_dir / f"{name}.mp4"

        if output_file.exists():
            print(f"[SKIP] Уже существует: {output_file}")
            continue

        run_translation(url, output_file, args.translator)


if __name__ == "__main__":
    main()