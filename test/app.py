
from flask import Flask, render_template_string
from flaskeztest import EZTest

# If testing reflection uncomment
# from sqlalchemy import select

# If testing reflection uncomment
# from model import db

# If testing declared model classes uncomment
from model import db, User

FLASK_APP_CONFIG = {
    # uncomment if testing reflection
    # 'EZTEST_REFLECTION_DB_URI': 'sqlite:///reflect.db',
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

    # If testing reflection uncomment
    # user = db.engine.execute(select([db.Model.metadata.tables['User']])).fetchone()

    # If testing declared models uncomment
    user = db.session.query(User).first()

    return render_template_string("""<p {{_eztestid('User.name')}}>{{user_name}}</p>
                                  <p {{_eztestid('User.email')}}>{{user_email}}</p>""",
                                  user_name=user.name, user_email=user.email)


@app.route('/two')
def index_two():

    # If testing reflection uncomment
    # users = db.engine.execute(select([db.Model.metadata.tables['User']])).fetchall()

    # If teseting declared model classes uncomment
    users = db.session.query(User).all()

    user_name1 = users[0].name
    user_name2 = users[1].name

    return render_template_string("""<p {{_eztestid('User.name', 0)}}>{{user_name1}}</p>
                                     <p {{_eztestid('User.name', 1)}}>{{user_name2}}</p>""",
                                  user_name1=user_name1, user_name2=user_name2)
