Flask EZ Test
=============

Making flask app that serve html and use a flasksqlalchemy backend engine easier to test

Setup
-----
.. code::
    $ pip install flaskeztest
    
Then run all test suites with eztest command

.. code::
    $ eztest

In General, the eztest object get's its settings from a special test config module which is set in app.config
as EZTEST_CONFIG_MODULE

I.E:

.. code:: python
    # test/config.py

    EZTEST_FIXTURES_DIR = 'test/fixtures'
    EZTEST_SUITES_PACKAGE = 'test/suites'

.. code:: python
    # config.py
    
    EZTEST_CONFIG_MODULE='test/config'
    ...
    
Then in flask app module set config from normal config module

.. code:: python
    # myapp.py
    app = Flask(__name__)
    app.from_object('config')

    
Developing Testcases
--------------------

Test cases are pacakged in modules that expose a 'suite' object in its global scope

Example suite 'index':

.. code:: python

    # test/suites/index.py
    from flaskeztest import EZTestSuite, EZTestCase

    class SimpleTestCase(EZTestCase):

        FIXTURE = 'myfixture'  # json filename without .json

        def runTest(self):
            self.assertTrue(...the truth...)

    ...

    suite = EZTestSuite('index', __name__)

Using Fixtures
--------------

Fixtures are a json file representing data to insert into the database before a test case runs

Example:

myfix.json
.. code:: json

    [
        {
            "model": "User",
            "row": {
                "name": "Bob",
                "email: "bob@example.com"
            }
        }
    ]

or with  multiple entries for one model:

myfix2.json
.. code:: json

    [
        {
            "model": "User",
            "rows": [
                {
                    "name": "Bob",
                    "email: "bob@example.com"
                },
                {
                    "name": "Alice",
                    "email: "alice@example.com"
                }
            ]
        }
    ]

The EZTestCase class
--------------------

EZTestCase's setUp method loads the fixture named in its FIXTURE class variable which places the data for each field
into the expected_models dict.

For instance:

class TC(EZTestCase):

    FIXTURE = 'myfix'  # Referring to the first fixture above

    def runTest(self):

        # Passes
        self.assertEqual(self.expected_models['User']['name'], 'Bob')


class TC2(EZTestCase):

    FIXTURE = 'myfix2' # Referring to the second fixture above

    def runTest(self):

        # Passes as well, but would give index error on first test case
        self.assertEqual(self.expected_models['User'][1]['name], 'Alice')

Two other useful method of the EZTestCase class is 'get_endpoint' and 'does_field_exist'.

Example:

    class TC(EZTestCase):
        FIXTURE = 'myfix2'
        def runTest(self):
            # Pull up user details for Alice
            self.get_endpoint('index.users', user_id=2)  # Assume that index.users take user primary key as argument

            # Assert we see second user on page
            self.assertTrue(self.does_field_exist('User', 'name', 1))

In general most of the methods defined for EZTestCase are useful to include in your own test case classes.
Check out flaskeztest/eztestcase.py for more of them.


Using capybara
--------------

Flaskeztest allows for querying the html returned from pages using capybara.
Check out the .. _docs: https://elliterate.github.io/capybara.py/ for all the useful methods that can be applied to the
the EZTestCase.page object.

Running with a reflected SQL database
-------------------------------------

Sometimes flaskeztest may be used with a flask app that is not using declarative models with sqlalchemy, but instead
want to simply use a database whose schema is contained within the remote database itself.

One can specify the remote database that flask-eztest should reflect by setting the EZTEST_REFLECTED_DB_URI in the test config module

i.e
.. code:: python
    # test/config.py
    ...
    EZTEST_REFLECTED_DB_URI = 'mysql://..."