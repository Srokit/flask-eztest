
from flask import Flask
from model import init_db, db
from os import environ
from flaskeztest.eztester import EZTester

FLASK_APP_CONFIG = {
    'EZTEST_FIXTURES_DIR': 'test/fixtures',
    'EZTEST_CSS_SELECTOR': '_eztestid'
}

app = Flask(__name__)
app.config.update(**FLASK_APP_CONFIG)

# Creates tables from classes in models as well
init_db(app)

PY_ENV = environ.get('PY_ENV')

if PY_ENV == 'test':
    eztester = EZTester()
    eztester.init_app_and_db(app, db)
