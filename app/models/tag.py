from app.models.base import BaseModel
from google.appengine.ext import ndb
import logging


class TagModel( BaseModel ):

    # id -> is the Tag here - we reuse the id property
    Count       = ndb.IntegerProperty( indexed=True, default=0 )

    @classmethod
    def create_or_update_tag(cls, tag):
        entity = TagModel.get_by_id(tag) or cls(id=tag)
        entity.Count += 1
        entity.put()
        return entity

    @classmethod
    def get_top_tags_async(cls):
        return cls.query().order( -cls.Count ).fetch_async(8)
