import handler

class LogoutPage(handler.Handler):
	"""
	Handler for user logout function.
	"""
	def get(self):
		next_url = self.request.headers.get('referer', '/')
		self.logout()
		self.redirect(next_url) # redirects to previous page
