from app.models.base import BaseModel
from app.models.tag import TagModel
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb
from app.common.utils import slugify
import logging



class ExplorerModel( BaseModel ):

	email				= ndb.StringProperty( indexed=True, required=True, )                  # this will the be the key - on new sign in's route to explorer create / update page
	displayName			= ndb.StringProperty( indexed=True, required=False, default='' )      # Explorer view
    uniqueId            = ndb.StringProperty( indexed=True, required=True )



	# countryCode		= ndb.StringProperty( indexed=True, required=True, )
	# deviceToken		= ndb.StringProperty( indexed=False, required=False )
	# appToken			= ndb.StringProperty( indexed=False, required=True ) # this is a unique id, generated when the app is launched the first time on a device
	# displayPicture	= ndb.BlobProperty(   indexed=False, required=False )

    @login_manager.user_loader
    def load_user(user_id):
        return ExplorerModel.get_by_id(user_id)
