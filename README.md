# Flask EZ Test
Making flask app that serve html and use a flasksqlalchemy backend engine easier to test

## Setup

Use you Flask and SQLAlchemy objects to initialize EZTest as eztest

    ## myapp.py
    from model import db
    app = Flask(__name__)
    eztest = EZTest()
    eztest.init_with_app_and_db(app, db)
    
Then run with eztest command

    $ eztest
    
This will run all EZTestCase subclasses defined in test modules named in flask app's config dict.

In General, the eztest object get's its settings from flask_app.config. So one should setup key values in there.

    ## config.py
    
    PY_ENV = 'test'
    EZTEST_FIXTURES_DIR = 'test/fixtures'
    EZTEST_TESTCASE_MODULE_PATHS = ['test/testcases.py', ...]
    
Then in flask app module

    ## myapp.py
    app = Flask(__name__)
    app.from_object('config')
    ...
    eztest = EZTest()
    eztest.init_with_app_and_db(app, db)
    
## Rendering Eztestids

Pattern for eztestids:

<model_name>[optional_index].<field_name> or <model_name>.<field_name>


A key to the way tests are run is that a special html dom attribute is rendered
into templates when testing mode is on for the flask app, but actaully 'rendered out'
of templates when in another mode.

Here's some example eztestid template syntax

    {# index.html #}
    
    <p {{_eztestid('mytestid.field')}}>something to test</p>
    
In test mode:
    
    <p _eztestid="mytestid.field">something to test</p>
    
In production mode:

    <p>something to test</p>
    
    
Optionally specify an index number as the second parameter to _eztestid if this template will
be tested against a fixture that has many rows to be inserted for a single model and the optional
index will be inserted for you.

    <p {{_eztestid('mytestid.field', 0)}}>something to test</p>
    <p {{_eztestid('mytestid.field', 1)}}>something to test</p>
    
In test mode becomes:

    <p _eztestid="mytestid[0].field">something to test</p>
    <p _eztestid="mytestid[1].field">something to test</p>
    
This is useful for iterating through lists in jinja 2
    
## Developing Testcases

Example testcase:

    ## testcase.py
    from flaskeztest import EZTestCase
    class SimpleTestCase(EZTestCase):
        FIXTURE = 'myfixture'
        def runTest(self):
            self.navigate_to_endpoint('index')
            self.assert_fixture_exists()
            
Check out EZTestCase class in flaskeztest/eztestcase.py module for assertion helper methods to use 

You can also just revert back to selenium DOM queries using the EZTestCase.driver property

## Decorating Routes

You can decorate a route using the expect_full_fixture method of EZTest class

    ## myapp.py
    app = Flask(__name__)
    
    ..[eztest initialization]..
    
    @app.route('/')
    @eztest.expect_full_fixture('myfixture')
    def index():
        return render_template_string('''<p {{_eztestid('Model.field')}}>
                    {{model_field}}</p>''', model_field=Model.field)
    