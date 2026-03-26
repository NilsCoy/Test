# 🗺️ Translate Video

Проект позволяет скачивать видео с сайтов или использовать локальные видео, автоматически распознавать речь, переводить её на русский язык и генерировать озвучку, создавая готовое видео с переводом.

---

## 📄 Основные функции

- Перевод видео по ссылке или через локальный файл
- Перевод видео списком (json)
- Поиск ссылок с видео на конкретном сайте

---

## 📦 Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/NilsCoy/Translate-Video.git
cd translate-video
```

### 2. Создание виртуального окружения

#### Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / Mac:

```bash
python -m venv venv
source venv/bin/activate
```
### 3. Установка библиотек

```bash
make install
```

### 4. Установка системных зависимостей

#### Windows:

```bash
make setup-win
```

#### Linux / Mac:

```bash
make setup-linux
```

## ⚡ Использование

### Перевод через Makefile

#### 1. Перевод видео по URL

```bash
make translate INPUT="https://example.com/video" OUTPUT="out.mp4" TRANSLATOR="v1"
```

#### 2. Перевод локального видео

```bash
make translate FILE="input.mp4" OUTPUT="out.mp4" TRANSLATOR="v1"
```

#### 3. Использовать альтернативный переводчик (v2)

```bash
make translate FILE="input.mp4" OUTPUT="out.mp4" TRANSLATOR="v2"
```

### Перевод через Python напрямую

#### URL:

```bash
python -m translate --input "https://example.com/video" --output "out.mp4" --translator "v1"
```

#### Локальный файл:

```bash
python -m translate --input "videos/input.mp4" --output "out.mp4" --translator "v1"
```

### Скачивание и перевод видео списком

#### Make:

```bash
make run-batch JSON="translate_videos.json" TRANSLATOR="v1" OUTPUT_DIR="outputs"
```

#### Через Python напрямую:

```bash
python -m batch_translate --json "translate_videos.json" --translator "v1" --output-dir "outputs"
```

### Получение списка видео через crawling:

#### Make:

```bash
make search-videos URL="https://example.com" OUTPUT="videos.json" MAX_PAGES=10
```

#### Через Python напрямую:

```bash
python -m search_videos --url "https://example.com" --output "videos.json" --max-pages 10
```

### Сохранение cookies для доступа к сайтам:

#### Make:

```bash
make save-cookies URL="https://example.com"
```

#### Через Python напрямую:

```bash
python -m save_cookies --url "https://example.com"
```