PYTHON=python

install:
	$(PYTHON) -m pip install -r requirements.txt

setup-linux:
	bash setup.sh

setup-win:
	powershell -ExecutionPolicy Bypass -File setup.ps1

# URL режим
run-url:
	$(PYTHON) -m main --input "$(INPUT)" --output "$(OUTPUT)" --translator "$(TRANSLATOR)"

# ЛОКАЛЬНЫЙ ФАЙЛ
run-file:
	$(PYTHON) -m main --input "$(FILE)" --output "$(OUTPUT)" --translator "$(TRANSLATOR)"

# МАССОВЫЙ ПЕРЕВОД ИЗ JSON
run-batch:
	$(PYTHON) batch_translate.py --json "$(JSON)" --translator "$(TRANSLATOR)" --output-dir "$(OUTPUT_DIR)"

# ПОИСК ВСЕХ ВИДЕО НА САЙТЕ
search-videos:
	$(PYTHON) search_videos.py --url "$(URL)" --output "$(OUTPUT)" --max-pages "$(MAX_PAGES)"

# СОХРАНЕНИЕ COOKIE ДЛЯ САЙТОВ
save-cookies:
	$(PYTHON) save_cookies.py --url "$(URL)"