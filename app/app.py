from . import config
from flask import Flask
from .common import utils
from flask.ext.login import LoginManager


app = Flask(__name__)
app.config.from_object(config)
app.jinja_env.globals['url_for_other_page'] = utils.url_for_other_page
app.jinja_env.filters['pretty_date'] = utils.pretty_date


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

from .views import views
