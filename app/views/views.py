from app.app import app, login_manager
from app.common.auth import OAuthSignIn
from app.common.pagination import Pagination
from app.common.testdata import create_posts
from app.forms.comment import CommentForm
from app.forms.post import PostForm
from app.models.explorer import ExplorerModel
from app.models.comment import CommentModel
from app.models.post import PostModel
from app.models.tag import TagModel
from flask import render_template, redirect, url_for, request
from flask.ext.login import login_user, logout_user, current_user, login_required
from google.appengine.ext import ndb
import logging


##################### OAUTH Related funcs ###############
@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    username, email = oauth.callback()
    if email is None:
        # I need a valid email address for my user identification
        logging.error('Authentication Failed')
        flash('Authentication failed.')
        return redirect(url_for('index'))
    # Look if the user already exists
    explorer = ExplorerModel.get_user_by_email(email)
    #user=User.query.filter_by(email=email).first()
    if not explorer:
        displayname = username
        if displayname is None or displayname == "":
            displayname = email.split('@')[0]

        # We can do more work here to ensure a unique nickname, if you
        # require that.
        explorer = ExplorerModel(Email=email, DisplayName=displayname)
        explorer.put()
    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    login_user(explorer, remember=True)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def render_page_or_error(template_name, context={}, error=None):
    """ helper function for routing to error page """
    if context:
        context.update({'user':current_user})
        return render_template(template_name, **context)
    else:
        return render_template('error404.html', error=error)

################# home page tasklet ###################
@ndb.tasklet
def _index_tasklet(pag):
    posts, tags = yield pag.get_posts_async(), TagModel.get_top_tags_async()
    raise ndb.Return((posts, tags))

def _get_index_context(page, query):
    pag         = Pagination(page, query)
    ctx_future  = _index_tasklet(pag)
    posts, tags = ctx_future.get_result() # evaluate tasklet and grab results
    return dict(pag=pag, posts=posts, tags=tags)

################### home endpoint ####################
def _explorerInfo(base='/'):
    user = users.get_current_user()
    name = "Hello, Explorer!"
    login_url = None
    logout_url = None
    if user:
        name = "Hello, %s"%user.nickname()
        logout_url = users.create_logout_url(base)
    else:
        login_url = users.create_login_url(base)
    assert bool(logout_url) ^ bool(login_url), 'both login and logout cannot be true at the same time'
    return dict(name=name, login_url=login_url, logout_url=logout_url)

@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def index(page):
    """ home page endpoint """
    context = _get_index_context(page, PostModel.get_posts_query())
    #context.update( _explorerInfo(url_for('index',page=page)) )
    #logging.error( context )
    return render_page_or_error('index.html', context)

################### tag endpoint ####################
@app.route('/tag/<tag>', defaults={'page': 1})
@app.route('/tag/<tag>/page/<int:page>')
def posts_by_tag(tag, page):
    """ tag page endpoint """
    context = _get_index_context(page, PostModel.get_tags_query(tag))
    context.update( _explorerInfo(url_for('posts_by_tag', tag=tag, page=page)) )
    #logging.error( context )
    return render_page_or_error('index.html', context)

@ndb.tasklet
def _post_tasklet(slug):
    post, comments = yield PostModel.get_by_id_async(slug), CommentModel.get_comment_by_slug_async(slug)
    raise ndb.Return((post, comments))

def _get_post_context(slug):
    ctx_future = _post_tasklet(slug)
    post, comments = ctx_future.get_result() # evaluate tasklet and grab results
    return dict(post=post, comments=comments)

################### Post endpoint ####################
@app.route('/post/<slug>', methods = ['GET', 'POST'])
def single_post(slug):
    """ given a slug, display the related page """
    context = _get_post_context(slug)
    commentform = CommentForm()
    if commentform.validate_on_submit():
        try:
            ncomment = CommentModel.create_comment(commentform, slug)
            return redirect(url_for('single_post', slug=slug))
        except Exception as e:
            return redirect(url_for('error404'))
    context.update({'commentform':commentform})
    context.update( _explorerInfo(url_for('single_post', slug=slug)) )
    return render_page_or_error('single_post.html', context)

@app.route('/error')
def error404():
    return render_template('error404.html')

################### Login endpoint ####################
# @app.route('/login')
# def login():
#     return render_template('login.html')

################# post editor endpoint ################
@app.route('/posteditor', methods = ['GET', 'POST'])
def posteditor():
    postform = PostForm()
    if postform.validate_on_submit():
        try:
            npost = PostModel.create_or_update_post(postform)
            return render_template('post_success.html', post=npost)
        except Exception as e:
            logging.error(str(e))
            return render_template('error404.html', error=str(e))
    else:
        return render_template('posteditor.html',postform=postform)

################## create sample data ##################
@app.route("/create_entries")
def EchosHome():
    create_posts()
    logging.error('%s: posts created' %__name__)
    return redirect( url_for('index') )
