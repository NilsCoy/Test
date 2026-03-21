


# translate V1

import whisper
from googletrans import Translator
from gtts import gTTS
from moviepy import VideoFileClip, AudioFileClip

def translate_v1(video_path: str, output_video: str) -> str:
    """Перевод полученного видео"""
    #video_path = "video.mp4"
    audio_path = "videos/temp/audio.wav"
    voice_path = "videos/temp/voice.mp3"
    #output_video = "translated_video_v1.mp4"

    VIDEOS_TEMP = "videos/temp"
    os.makedirs(VIDEOS_TEMP, exist_ok=True)

    print("\n\n1. Извлекаем аудио")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

    print("\n\n2. Распознаем речь")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)

    text = result["text"]
    print("Original:", text)

    print("\n\n3. Перевод текста")
    translator = Translator()
    translated = translator.translate(text, dest="ru").text

    print("Translated:", translated)

    print("\n\n4. Генерация озвучки")
    tts = gTTS(translated, lang="ru")
    tts.save(voice_path)

    print("\n\n5. Вставляем новую озвучку")
    new_audio = AudioFileClip(voice_path)
    final_video = video.with_audio(new_audio)

    final_video.write_videofile(output_video)

    return output_video



# translate V2

import os
import whisper
from googletrans import Translator
from gtts import gTTS
from moviepy import VideoFileClip, AudioFileClip, concatenate_audioclips
import contextlib

def translate_v2(video_path: str, output_video: str) -> str:
    """Перевод полученного видео частями, чтобы речь была синхронна с видео"""
    #video_path = "video.mp4"
    temp_dir = "videos/temp/temp_audio"
    audio_path = "videos/temp/audio.wav"
    #output_video = "translated_video_v2.mp4"

    VIDEOS_TEMP = "videos/temp"
    os.makedirs(VIDEOS_TEMP, exist_ok=True)

    os.makedirs(temp_dir, exist_ok=True)

    print('\n\n1. Извлекаем аудио')
    video = VideoFileClip(video_path)
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)

    print('\n\n2. Распознаем речь с таймкодами')
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, word_timestamps=True)

    segments = result["segments"]  # каждый сегмент содержит 'start', 'end', 'text'

    translator = Translator()
    audio_clips = []

    print('\n\n3. Генерация озвучки для каждого сегмента')
    for i, seg in enumerate(segments):
        text_ru = translator.translate(seg['text'], dest='ru').text
        tts = gTTS(text_ru, lang='ru')
        temp_path = os.path.join(temp_dir, f"segment_{i}_{seg['start']:.2f}.mp3")

        # Подавляем вывод
        with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
            tts.save(temp_path)

        clip = AudioFileClip(temp_path)
        duration = seg['end'] - seg['start']
        clip = clip.set_duration(duration)
        audio_clips.append(clip)

    print('\n\n4. Объединяем сегменты')
    final_audio = concatenate_audioclips(audio_clips)

    print('\n\n5. Вставляем озвучку в видео')
    final_video = video.with_audio(final_audio)
    final_video.write_videofile(output_video)

    print('\n\n6. Очистка временных файлов')
    for f in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, f))
    os.rmdir(temp_dir)

    return output_video