
app:
	pyinstaller xl8.spec --noconfirm

venv: requirements.txt
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt
