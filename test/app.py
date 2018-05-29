
from flask import Flask, render_template_string
from flaskeztest import EZTest, FixtureExpectation, ModelExpectation, FieldExpectation, expect_fixture

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

twousers_User_name_expected = FixtureExpectation('twousers').models([ModelExpectation('User').
                                                                    not_fields(['email'])])

oneuser_User_name_and_email_expected = expect_fixture('oneuser').models([ModelExpectation('User').
                                                                         not_fields(['hidden'])])

oneuser_visible_hidden_field = expect_fixture('oneuser').models([ModelExpectation('User')
                                                                .fields([FieldExpectation('hidden').invisible(), 'email', 'name'])])


@app.route('/one')
# @eztest.expect_model('oneuser', 'User', exclude_fields=['hidden'])
# @eztest.expect(oneuser_User_name_and_email_expected)
@eztest.expect_model('oneuser', 'User')
@eztest.expect_model('oneuser', 'User')
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
# @eztest.expect_full_fixture('twousers', exclude_fields=['User.email', 'User.hidden'])
@eztest.expect(twousers_User_name_expected)
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


@app.route('/one_visible')
@eztest.expect(oneuser_visible_hidden_field)
def one_visible():
    user = db.session.query(User).first()

    return render_template_string("""<p {{_eztestid('User.name')}}>{{user_name}}</p>
                                  <p {{_eztestid('User.email')}}>{{user_email}}</p>
                                  <p {{_eztestid('User.hidden')}} style="display: block">{{user_hidden}}</p>
                                    <script>
                                             setTimeout(function(){
                                                document.getElementsByTagName('p')[2].style.display = 'block';
                                             }, 500);
                                     </script>
                                  """, user_name=user.name, user_email=user.email, user_hidden=user.hidden)
