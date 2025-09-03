setup:
	python3 -m venv venv
	source venv/bin/activate
	pip3 install -r requirements.txt

lint:
	isort app
	python3 -m black . -l 120

debug:
	FLASK_APP=app:app venv/bin/flask --debug run --port 8000

run:
	FLASK_APP=app:app venv/bin/flask run --port 8000