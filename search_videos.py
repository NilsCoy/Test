from re import search

from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse, urlunparse
import json
import argparse

def find_videos(page, base_url):
    """
    Ищет любое видео со страницы.
    Поддерживаются mp4, webm, m3u8.
    """
    video_urls = set()

    def handle_response(response):
        url = response.url
        if any(ext in url for ext in [".mp4", ".webm", ".m3u8"]):
            video_urls.add(url)

    page.on("response", handle_response)
    page.goto(base_url, timeout=60000)
    page.wait_for_timeout(5000)

    return video_urls


def get_links(page, base_url):
    """
    Собирает все ссылки с текущей страницы, только с того же домена.
    Поддерживаются <a>, <img>, <script>, <iframe>.
    """
    links = set()

    elements = page.query_selector_all("a, img, script, iframe")

    for el in elements:
        href = el.get_attribute("href") or el.get_attribute("src")
        if not href:
            continue

        href = href.strip()
        if not href or href.startswith(("#", "mailto:", "tel:")):
            continue

        full_url = urljoin(base_url, href)

        if urlparse(full_url).netloc != urlparse(base_url).netloc:
            continue

        parsed = urlparse(full_url)
        normalized = urlunparse(parsed._replace(query=""))

        links.add(normalized)

    return links

def crawl(start_url, max_pages=10, file_path = "videos.json"):
    """
    Идет по странице и ищет видео на них.
    """
    visited = set()
    to_visit = [start_url]

    results = {}
    video_count = 1

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        try:
            with open("cookies.json", "r", encoding="utf-8") as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
        except Exception as e:
            print(f"Ошибка загрузки cookies: {e}")

        while to_visit and len(visited) < max_pages:
            url = to_visit.pop(0)

            if url in visited:
                continue

            print(f"Открываем: {url}")
            visited.add(url)

            page = context.new_page()

            try:
                # ищем видео
                videos = find_videos(page, url)
                # video_urls = set()
                #
                # def handle_response(response):
                #     response_url = response.url
                #     if any(ext in response_url for ext in [".mp4", ".webm", ".m3u8"]):
                #         video_urls.add(response_url)
                #         print(response_url)
                #
                # page.on("response", handle_response)
                #
                # page.goto(url, timeout=60000)
                # page.wait_for_timeout(10000)
                #
                # print(video_urls)

                if videos:
                    results[f"video_{video_count}"] = url
                    video_count += 1
                    print("[+] Найдено видео!")

                save_data(file_path, results)

                # собираем новые ссылки
                links = get_links(page, url)

                for link in links:
                    if link not in visited:
                        to_visit.append(link)

            except Exception as e:
                print(f"Ошибка: {e}")

            page.close()
        browser.close()

    return results

def save_data(file_path = "videos.json", data = {}):
    """
    Сохраняет данные в файл
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="Поиск видео на сайте")

    parser.add_argument(
        "--url",
        type=str,
        help="Ссылка на сайт для сканирования"
    )

    parser.add_argument(
        "--output",
        type=str,
        nargs="?",
        default="videos.json",
        help="Файл для сохранения результатов (по умолчанию videos.json)"
    )

    parser.add_argument(
        "--max-pages",
        type=int,
        default=10,
        help="Максимальное количество страниц (по умолчанию 10)"
    )

    args = parser.parse_args()

    print(f"Старт: {args.url}")
    print(f"Файл: {args.output}")
    print(f"Макс. страниц: {args.max_pages}")

    data = crawl(args.url, max_pages=args.max_pages, file_path=args.output)

    print(f"Готово! Найдено видео: {len(data)}")
    print(f"Сохранено в {args.output}")

if __name__ == "__main__":
    # url = "https://learn.deeplearning.ai/courses/a2a-the-agent2agent-protocol/lesson/vtf72ap4/introduction"
    # url = 'https://learn.deeplearning.ai/courses/a2a-the-agent2agent-protocol/lesson/3sqlzg/creating-a-multi-agent-system-using-a2a-with-beeai-framework'
    # url = "https://anthropic.skilljar.com/claude-code-in-action/303239"
    # data = crawl(url, 10)
    # print("Готово! Сохранено в videos.json")

    main()