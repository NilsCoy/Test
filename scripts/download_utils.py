


# yt_dlp

import yt_dlp

def yt_dlp_download(url: str) -> str:
    #url = "https://learn.deeplearning.ai/courses/a2a-the-agent2agent-protocol/lesson/vtf72ap4/introduction"

    DOWNLOAD_DIR = "videos"
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    ydl_opts = {
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"), #"video.%(ext)s"
        "cookies": "cookies.txt",
        "format": "best",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        filename = ydl.prepare_filename(info)
        ydl.download(url)
        return filename



# playwright

import asyncio
import os
import subprocess
from playwright.async_api import async_playwright
import nest_asyncio

def playwright_download(url: str) -> str:
    DOWNLOAD_DIR = "videos"
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    found_urls = set()
    result_file = {"path": None}

    async def download_and_convert(video_url):
        filename = os.path.join(DOWNLOAD_DIR, "video.mp4")
        mp3_file = os.path.join(DOWNLOAD_DIR, "audio.mp3")

        print(f"\nDownloading: {video_url}")

        # Скачивание через ffmpeg
        subprocess.run([
            "ffmpeg",
            "-y",
            "-i", video_url,
            "-c", "copy",
            filename
        ])

        print("Converting to mp3...")

        subprocess.run([
            "ffmpeg",
            "-y",
            "-i", filename,
            "-q:a", "0",
            "-map", "a",
            mp3_file
        ])

        print("Done:", mp3_file)

        # сохраняем итоговый файл
        result_file["path"] = mp3_file

    async def run():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            async def handle_request(request):
                req_url = request.url

                if any(ext in req_url for ext in [".m3u8", ".mp4"]):
                    if req_url not in found_urls:
                        found_urls.add(req_url)
                        print("\nVideo:", req_url)

                        await download_and_convert(req_url)

            page.on("request", handle_request)

            await page.goto(url)
            await page.wait_for_timeout(5000)

            try:
                await page.click('[aria-label="Play"]')
            except:
                pass

            await page.wait_for_timeout(20000)
            await browser.close()

    nest_asyncio.apply()
    asyncio.run(run())

    return result_file["path"]