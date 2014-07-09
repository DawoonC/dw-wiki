import utils
from google.appengine.ext import db

class User(db.Model):
	"""
	Users signed up at the DW WIKI.
	The users are stored in Google Data Store.
	"""
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email = db.StringProperty() # e-mail property is optional

	@classmethod
	def by_id(cls, uid):
		return User.get_by_id(uid, parent = utils.users_key())

	@classmethod
	def by_name(cls, name):
		user = User.all().filter('username =', name).get()
		return user

	@classmethod
	def register(cls, name, pw, email = None):
		pw_hash = utils.make_pw_hash(name, pw)
		return User(parent = utils.users_key(),
					username = name,
					password = pw_hash,
					email = email)

	@classmethod
	def login(cls, name, pw):
		user = cls.by_name(name)
		if user and utils.valid_pw(name, pw, user.password):
			return user
