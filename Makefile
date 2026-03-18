PYTHON=python

install:
	pip install -r requirements.txt

setup-linux:
	bash setup.sh

setup-win:
	powershell -ExecutionPolicy Bypass -File setup.ps1

# URL режим
run-url:
	$(PYTHON) -m main --input "$(INPUT)" --output "$(OUTPUT)"

# ЛОКАЛЬНЫЙ ФАЙЛ
run-file:
	$(PYTHON) -m main --input "$(FILE)" --output "$(OUTPUT)"