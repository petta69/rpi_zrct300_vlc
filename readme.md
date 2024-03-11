
Install python modules:
pip install -r requirements.txt

Start with gunicorn:
gunicorn --config gunicorn_config.py app:app