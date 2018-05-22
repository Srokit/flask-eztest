
from flask import Flask, render_template_string
from flaskeztest import EZTest

from model import db, User

# from testmod import run

FLASK_APP_CONFIG = {
    'EZTEST_FIXTURES_DIR': 'test/fixtures',
    'EZTEST_TESTCASE_MODULE_PATHS': ['test/testcases.py', 'test/fail_testcases.py'],
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'PY_ENV': 'test'
}

app = Flask(__name__)
app.config.update(**FLASK_APP_CONFIG)

eztest = EZTest()
eztest.init_with_app_and_db(app, db)


@app.route('/one')
@eztest.expect_full_fixture('oneuser')
def index_one():

    user = db.session.query(User).first()

    return render_template_string("""<p {{_eztestid('User.name')}}>{{user_name}}</p>
                                  <p {{_eztestid('User.email')}}>{{user_email}}</p>""",
                                  user_name=user.name, user_email=user.email)


@app.route('/two')
def index_two():

    users = db.session.query(User).all()
    user_name1 = users[0].name
    user_name2 = users[1].name

    return render_template_string("""<p {{_eztestid('User.name', 0)}}>{{user_name1}}</p>
                                     <p {{_eztestid('User.name', 1)}}>{{user_name2}}</p>""",
                                  user_name1=user_name1, user_name2=user_name2)
