
from flask import Flask, render_template_string
# from model import init_db, db
from os import environ
from flaskeztest import EZTestTemplater

# from testmod import run

FLASK_APP_CONFIG = {
    'EZTEST_FIXTURES_DIR': 'test/fixtures',
    'EZTEST_CSS_SELECTOR': '_eztestid',
    'PY_ENV': 'nottest'
}

app = Flask(__name__)
app.config.update(**FLASK_APP_CONFIG)

eztest_templater = EZTestTemplater()

eztest_templater.init_app(app)

# Creates tables from classes in models as well
# init_db(app)

PY_ENV = environ.get('PY_ENV')

# eztester = EZTester()
#
# class NewTC(EZTestCase):
#
#     def runTest(self):
#         driver = eztester.get_client_after_loading_fixture('simple')
#         driver.startup_driver()
#         driver.get_driver().get('http://localhost:5000/')
#         print driver.get_driver().page_source
#         driver.assert_exists('Table1[1].name')
#         driver.assert_has_correct_val('Table1[1].name')
#
#
# class New2TC(EZTestCase):
#     pass
#
#


@app.route('/')
def index():

    return '<p _eztestid=Table1[1].name {{_eztestid(\'sup\')}}>Stan</p>'
#


@app.route('/test')
def index_test():
    print "in index test"
    print render_template_string('{{test}} {{test2}}', test='sup', test2='sup2')
    return render_template_string('{{test}}', test='sup')
#
# if PY_ENV == 'test':
#     eztester.init_app_and_db(app, db)
#     eztester.print_all_subclasses()
#     eztester.run_tests_and_exit(run)
