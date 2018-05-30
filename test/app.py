
from flask import Flask, render_template_string

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
    'EZTEST_TESTCASE_MODULE_PATHS': ['test/testcases.py'],
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'PY_ENV': 'test'
}

app = Flask(__name__)
app.config.update(**FLASK_APP_CONFIG)

db.init_app(app)


@app.route('/one')
def index_one():

    # If testing reflection uncomment
    # user = db.engine.execute(select([db.Model.metadata.tables['User']])).fetchone()

    # If testing declared models uncomment
    user = db.session.query(User).first()

    return render_template_string("""<p style="display:none">{{user_name}}</p>
                                  <p>{{user_email}}</p>""",
                                  user_name=user.name, user_email=user.email)


@app.route('/two')
def index_two():

    # If testing reflection uncomment
    # users = db.engine.execute(select([db.Model.metadata.tables['User']])).fetchall()

    # If teseting declared model classes uncomment
    users = db.session.query(User).all()

    user_name1 = users[0].name
    user_name2 = users[1].name

    return render_template_string("""<p>{{user_name1}}</p>
                                     <p>{{user_name2}}</p>""",
                                  user_name1=user_name1, user_name2=user_name2)


@app.route('/one_visible')
def one_visible():
    user = db.session.query(User).first()

    return render_template_string("""<p>{{user_name}}</p>
                                  <p>{{user_email}}</p>
                                  <p style="display: block">{{user_hidden}}</p>
                                    <script>
                                             setTimeout(function(){
                                                document.getElementsByTagName('p')[2].style.display = 'block';
                                             }, 500);
                                     </script>
                                  """, user_name=user.name, user_email=user.email, user_hidden=user.hidden)
