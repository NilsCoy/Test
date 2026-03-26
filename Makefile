PYTHON=python

install:
	$(PYTHON) -m pip install -r requirements.txt

setup-linux:
	bash setup.sh

setup-win:
	powershell -ExecutionPolicy Bypass -File setup.ps1

# Перевод
translate:
	$(PYTHON) -m translate --input "$(INPUT)" --output "$(OUTPUT)" --translator "$(TRANSLATOR)"

# МАССОВЫЙ ПЕРЕВОД ИЗ JSON
run-batch:
	$(PYTHON) -m batch_translate --json "$(JSON)" --translator "$(TRANSLATOR)" --output-dir "$(OUTPUT_DIR)"

# ПОИСК ВСЕХ ВИДЕО НА САЙТЕ
search-videos:
	$(PYTHON) -m search_videos --url "$(URL)" --output "$(OUTPUT)" --max-pages "$(MAX_PAGES)"

# СОХРАНЕНИЕ COOKIE ДЛЯ САЙТОВ
save-cookies:
	$(PYTHON) -m save_cookies --url "$(URL)"