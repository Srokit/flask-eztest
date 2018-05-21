
from flask import Flask, render_template_string

from flaskeztest import EZTest

# from testmod import run

FLASK_APP_CONFIG = {
    'EZTEST_FIXTURES_DIR': 'test/fixtures',
    'EZTEST_CSS_SELECTOR': '_eztestid',
    'PY_ENV': 'nottest'
}

app = Flask(__name__)
app.config.update(**FLASK_APP_CONFIG)

eztest = EZTest()
eztest.init_app(app)


@app.route('/')
def index():

    return '<p _eztestid=Table1[1].name {{_eztestid(\'sup\')}}>Stan</p>'
