import handler
from data import Wiki

class HistoryPage(handler.Handler):
	"""
	Handler for the history page.
	History page contains modifcation history of the wiki page.
	"""
	def get(self, path):
		entities = Wiki.Wiki.by_path(path)
		entities.fetch(limit=50)

		posts = list(entities)
		if posts:
			self.render("wiki_history.html", path=path, posts=posts)
		else:
			self.redirect("/_edit" + path)
