import handler
import utils
from data import User

class SignupPage(handler.Handler):
	"""
	Handler for user signup function.
	Signed up user will be stored in DB.
	"""
	def get(self):
		next_url = self.request.headers.get('referer', '/')
		self.render("wiki_signup.html", next_url=next_url)

	def post(self):
		have_error = False

		next_url = str(self.request.get('next_url'))
		if not next_url or next_url.startswith('/login'):
			next_url = '/'

		self.username = self.request.get('username')
		self.password = self.request.get('password')
		self.verify = self.request.get('verify')
		self.email = self.request.get('email')

		params = dict(username = self.username,
					  email = self.email)

		if not utils.valid_username(self.username):
			params['error_username'] = "That's not a valid username."
			have_error = True

		if not utils.valid_password(self.password):
			params['error_password'] = "That wasn't a valid password."
			have_error = True
		elif self.password != self.verify:
			params['error_verify'] = "Your passwords didn't match."
			have_error = True

		if not utils.valid_email(self.email):
			params['error_email'] = "That's not a valid email."
			have_error = True

		if have_error:
			self.render('wiki_signup.html', **params)
		else:
			self.done()

	def done(self, *a, **kw):
		raise NotImplementedError


class Register(SignupPage):
	def done(self):
		next_url = str(self.request.get('next_url'))
		if not next_url or next_url.startswith('/login'):
			next_url = '/'

		user = User.User.by_name(self.username)
		if user:
			error = 'That user already exists.'
			self.render('wiki_signup.html', error_username = error)
		else:
			user = User.User.register(self.username, self.password, self.email)
			user.put()

			self.login(user)
			self.redirect(next_url) # redirects to previous page
