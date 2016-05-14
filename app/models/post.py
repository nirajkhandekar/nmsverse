from app.models.base import BaseModel
from app.models.tag import TagModel
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb
from app.common.utils import slugify
import logging


class PostModel( BaseModel ):

    Title       = ndb.StringProperty( indexed=True, required=True )
    Post        = ndb.BlobProperty( indexed=False, required=True )
    Description = ndb.BlobProperty( indexed=False )
    Tags        = ndb.StringProperty( indexed=True, repeated=True )
    Likes       = ndb.IntegerProperty( indexed=True, default=0 )
    Author      = ndb.StringProperty(indexed=True, default="nck87" )
    Published   = ndb.BooleanProperty( indexed=True, required=True)

    def save_post(self, **kwargs):
        try:
            post = PostModel(**kwargs)
            post.put()
        except Exception as e:
            logging.info(e)
        else:
            return post

    @classmethod
    def create_or_update_post(cls, postForm):
        slug = slugify(postForm.title.data)
        post = PostModel.get_by_id(slug)
        if not post:
            tags = list()
            rawtag = str(postForm.tags.data).strip()
            if "," in rawtag:
                for tag in rawtag.split(","):
                    tags.append(tag.strip())
            else:
                tags.append(rawtag)
            post = PostModel(
                                id          = slug,
                                Title       = str(postForm.title.data),
                                Post        = str(postForm.post.data),
                                Description = str(postForm.description.data),
                                Tags        = tags,
                                Published   = True,
                            )
            post.put()
            for tg in tags:
                TagModel.create_or_update_tag(tg)
        return post

    @classmethod
    def get_posts_query(cls):
        return cls.query().order(-cls.created)

    @classmethod
    def get_tags_query(cls, tag, page=None):
        return cls.query(cls.Tags.IN([tag])).order(-cls.created)

    @classmethod
    def get_post_by_slug_async(cls, slug):
        return PostModel.get_by_id_async(slug)

    @classmethod
    def query_posts(cls, page=None, tag=None, search=None):
        # we support tag or search - search will be using or condition
        cursor = Cursor(urlsafe=page)
        cond = []
        if search:
            cond += [ cls.Title == search ]
        if tag:
            cond += [ cls.Tags == tag ]
        query = cls.query(ndb.OR(tuple(cond))).order(-cls.created)
        iterRes, nextCurs, more = query.fetch_page(10, start_cursor=cursor)
        return iterRes, nextCurs, more
