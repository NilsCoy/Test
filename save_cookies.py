
from playwright.sync_api import sync_playwright
import json
import argparse

def login(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            with open("cookies.json", "r", encoding="utf-8") as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
        except Exception as e:
            print(f"Ошибка загрузки cookies: {e}")

        page.goto(url)

        input("Нажми Enter, чтобы закончить сохранение...")

        cookies = context.cookies()
        with open("cookies.json", "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2)

        browser.close()

def main():
    parser = argparse.ArgumentParser(description="Сохранение cookies")

    parser.add_argument(
        "--url",
        type=str,
        help="Ссылка на сайт"
    )

    args = parser.parse_args()

    print(f"Сайт: {args.url}")

    login(args.url)

    print(f"Готово!")

if __name__ == "__main__":
    main()