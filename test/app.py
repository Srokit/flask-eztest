
from flask import Flask, render_template_string
from flaskeztest import EZTest

from model import db, Table1

# from testmod import run

FLASK_APP_CONFIG = {
    'EZTEST_FIXTURES_DIR': 'test/fixtures',
    'EZTEST_TESTCASE_MODULE_PATHS': ['test/testcase.py'],
    'PY_ENV': 'test'
}

app = Flask(__name__)
app.config.update(**FLASK_APP_CONFIG)

eztest = EZTest()
eztest.init_with_app_and_db(app, db)


@app.route('/')
@eztest.expect_full_fixture('simple2')
def index():

    stan_name = db.session.query(Table1).first().name

    return render_template_string("<p {{_eztestid('Table1.name')}}>{{stan_name}}</p>", stan_name=stan_name)


@app.route('/2')
def index_2():

    stans = db.session.query(Table1).all()
    stan_name1 = stans[0].name
    stan_name2 = stans[1].name

    return render_template_string("""<p {{_eztestid('Table1.name', 0)}}>{{stan_name1}}</p>
                                     <p {{_eztestid('Table1.name', 1)}}>{{stan_name2}}</p>""",
                                  stan_name1=stan_name1, stan_name2=stan_name2)
