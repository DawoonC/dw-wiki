import handler
from data import User

class LoginPage(handler.Handler):
	"""
	Handler for user login function.
	"""
	def get(self):
		next_url = self.request.headers.get('referer', '/')
		self.render("wiki_login.html", next_url=next_url)

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")

		next_url = str(self.request.get('next_url'))
		if not next_url or next_url.startswith('/login'):
			next_url = '/'

		user = User.User.login(username, password)
		if user:
			self.login(user)
			self.redirect(next_url)
		else:
			error = 'Invalid login'
			self.render("wiki_login.html", error=error)
