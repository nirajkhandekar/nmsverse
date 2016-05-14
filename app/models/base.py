from google.appengine.ext import ndb
from app import config

class BaseModel( ndb.Model ):
	"""
	Abstract Model for each resource.
	"""

	created 		= ndb.DateTimeProperty( auto_now_add=True, indexed=True )
	updated 		= ndb.DateTimeProperty( auto_now=True, indexed=True )
	version 		= ndb.StringProperty( default=config.CURRENT_VERSION_NAME, indexed=False )
