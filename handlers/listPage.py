import handler

class ListPage(handler.Handler):
	"""
	Handler for the list page.
	This page contains list of all the wiki pages with their latest version.
	This page might not be updated quickly as expected due to memcache lag.
	(shared memcache is slow sometimes)
	"""
	def get(self):
		list_page = self.list_cache() # get the memcached list page

		if list_page:
			self.render("wiki_list.html", list_page=list_page)
		else:
			self.notfound()
