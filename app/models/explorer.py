from app.app import login_manager
from app.models.base import BaseModel
from app.models.tag import TagModel
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb
from app.common.utils import slugify
import logging
from flask.ext.login import UserMixin


class ExplorerModel( UserMixin, BaseModel ):

	Email				= ndb.StringProperty( indexed=True, required=True, )
	DisplayName			= ndb.StringProperty( indexed=True, required=False, default='' )
	#UniqueId            = ndb.StringProperty( indexed=True, required=True )

	# countryCode		= ndb.StringProperty( indexed=True, required=True, )
	# deviceToken		= ndb.StringProperty( indexed=False, required=False )
	# appToken			= ndb.StringProperty( indexed=False, required=True ) # this is a unique id, generated when the app is launched the first time on a device
	# displayPicture	= ndb.BlobProperty(   indexed=False, required=False )

	@classmethod
	def get_user_by_email(cls, email):
		query = cls.query( cls.Email==email )
		return query.fetch()


	def get_id(self):
		return self.key.id()

@login_manager.user_loader
def load_user(id):
	return ExplorerModel.get_by_id(id)
