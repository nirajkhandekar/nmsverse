from app.models.base import BaseModel
from google.appengine.ext import ndb
import logging


class CommentModel( BaseModel ):

    Name        = ndb.StringProperty(indexed=True, required=True)
    Email       = ndb.StringProperty(indexed=False, required=True)
    Comment     = ndb.BlobProperty(indexed=False, required=True)
    Published   = ndb.BooleanProperty(indexed=True, required=True)
    SlugId      = ndb.StringProperty(indexed=True, required=True)

    '''
        A user will enter a comment for a particular post - eg: ABC.
        We require the username, email, and comment information from the user.
        The comment will be set to published once reviewed - this will be false by default
        PostId will the be reference back to the comments
        Comments will also require pagination - since we will only show 10 comments at a time.
        Perhaps a show more click would do....
    '''

    def save_comment(self, **kwargs):
        ''' default save comment helper '''
        try:
            comment = CommentModel(**kwargs)
            comment.put()
        except Exception as e:
            logging.info(e)
            return None
        else:
            return comment

    @classmethod
    def create_comment(cls, commentForm, slug):
        """ create a comment tied to a post """
        comment = CommentModel(
                                Name        = str(commentForm.name.data),
                                Email       = str(commentForm.email.data),
                                Comment     = str(commentForm.comment.data),
                                Published   = True,
                                SlugId      = slug
                                )
        comment.put()
        return comment

    @classmethod
    def get_comment_by_slug_async(cls, slug):
        query = cls.query( cls.SlugId==slug )
        query = query.filter(cls.Published==True)
        return query.order(-cls.created).fetch_async()

    @classmethod
    def get_comment_by_username(cls, username):
        ''' returns all the comments for a user - sorted desc by creation time '''
        return cls.query( ndb.AND(tuple([cls.Name==username, cls.Published==True])) ).order(-cls.created)
