from . import config
from flask import Flask, render_template
from .models import post
from .common import utils
from flask.ext.login import LoginManager
from rauth.service import OAuth2Service
import logging


app = Flask(__name__)
app.config.from_object(config)
app.jinja_env.globals['url_for_other_page'] = utils.url_for_other_page
app.jinja_env.filters['pretty_date'] = utils.pretty_date


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"


google = OAuth2Service(name='google',
                       authorize_url='https://accounts.google.com/o/oauth2/auth',
                       access_token_url='https://accounts.google.com/o/oauth2/token',
                       client_id=app.config['GOOGLE_CLIENT_ID'],
                       client_secret=app.config['GOOGLE_CLIENT_SECRET'],
                       base_url=None)

logging.error(google)

from .views import views
