import utils
from google.appengine.ext import db

class Wiki(db.Model):
	"""
	Wiki pages submitted by users.
	The pages are stored in Google Data Store.
	"""
	subject = db.StringProperty() # subject of the page, default is the URL path
	content = db.TextProperty(required = True) 
	author = db.StringProperty(required = True) 
	#author = db.ReferenceProperty(User, required = True)  # assign User object from db, not applicable yet.
	submitted = db.DateTimeProperty(auto_now_add = True)  # auto_now_add automatically sets current time.
	last_modified = db.DateTimeProperty(auto_now = True)

	def render(self):
		self._render_text = self.content.replace('\n', '<br>')
		return utils.render_str("post.html", p = self)

	@staticmethod
	def parent_key(path):
		return db.Key.from_path('/root' + path, 'wikis')

	@classmethod
	def by_path(cls, path):
		entities = cls.all()
		entities.ancestor(cls.parent_key(path))
		entities.order("-submitted")
		return entities

	@classmethod
	def by_id(cls, page_id, path):
		return cls.get_by_id(page_id, cls.parent_key(path))
