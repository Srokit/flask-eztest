
from flask import Flask, render_template_string
from flaskeztest import EZTest

from model import db, Table1

# from testmod import run

FLASK_APP_CONFIG = {
    'EZTEST_FIXTURES_DIR': 'test/fixtures',
    'EZTEST_CSS_SELECTOR': '_eztestid',
    'PY_ENV': 'test',
    'EZTEST_SQLITE_DB_URI': 'test/test.db'
}

app = Flask(__name__)
app.config.update(**FLASK_APP_CONFIG)

eztest = EZTest()
eztest.init_with_app_and_db(app, db)


@app.route('/')
def index():

    stan_name = db.session.query(Table1).first().name

    return render_template_string("<p {{_eztestid('Table1[0].name')}}>Stan</p>")
