
from flask import Flask

FLASK_APP_CONFIG = {
    # TODO: Fill with data
}

app = Flask(__name__)
app.config.update(**FLASK_APP_CONFIG)
