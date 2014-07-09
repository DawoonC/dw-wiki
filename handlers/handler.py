import webapp2
import utils
from data import User, Wiki

from google.appengine.api import memcache

class Handler(webapp2.RequestHandler):
	"""
	Base handler for all other handlers.
	Contains handler methods for its subclasses.
	"""
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		params['user'] = self.user # this user is logged in user
		t = utils.jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def set_secure_cookie(self, name, val):
		cookie_val = utils.make_secure_val(val)
		self.response.headers.add_header(
			'Set-Cookie',
			'%s=%s; Path=/' % (name, cookie_val))

	def read_secure_cookie(self, name):
		cookie_val = self.request.cookies.get(name)
		return cookie_val and utils.check_secure_val(cookie_val)

	def login(self, user):
		self.set_secure_cookie('user_id', str(user.key().id()))

	def logout(self):
		self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		uid = self.read_secure_cookie('user_id')
		self.user = uid and User.User.by_id(int(uid))

		if self.request.url.endswith('.json'):
			self.format = 'json'
		else:
			self.format = 'html'

	def notfound(self):
		self.error(404)
		self.write("<h1><em>Dude, This page does not exist yet.</em></h1>")

	def version_check(self, path):
		version = self.request.get('version')
		page = None
		if version:
			if version.isdigit():
				page = Wiki.Wiki.by_id(int(version), path)

			if not page:
				return self.notfound()
		else:
			page = Wiki.Wiki.by_path(path).get()
		return page

	def list_cache(self, update = False):
		"""memcache for the list page."""
		key = 'list_page'
		list_page = memcache.get(key)
		if list_page is None or update:
			entities = Wiki.Wiki.all().order('-submitted')
			entities.fetch(limit=100)

			posts = list(entities)
			post_list = []
			list_page = []
			for e in posts:
				if e.subject not in post_list:
					post_list.append(e.subject)
					list_page.append(e)

			memcache.set(key, list_page)
		return list_page

	def flush(self):
		memcache.flush_all()

