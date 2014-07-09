import handler

class FlushCache(handler.Handler):
	def get(self):
		self.flush()
		self.redirect("/")
