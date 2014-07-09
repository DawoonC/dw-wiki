import handler
from data import Wiki

class EditPage(handler.Handler):
	"""
	Handler for the edit page.
	Edit can be edit of new page, and also can be edit of previous page.
	To edit the page, user must be logged in.
	"""
	def get(self, path):
		if not self.user:
			self.redirect('/login')

		page = self.version_check(path)

		if page:
			self.render("wiki_edit.html", exist=True, path=path, page=page)
		else:
			self.render("wiki_edit.html", exist=False, path=path, page=page)


	def post(self, path):
		if not self.user:
			self.error(400)
			return

		content = self.request.get('content')
		old_page = Wiki.Wiki.by_path(path).get()
		subject = self.request.get('subject')

		if path == '/_newpost': # this block is for "Newpost" button on the page. 
			if subject and content:
				page = Wiki.Wiki(parent = Wiki.Wiki.parent_key('/%s' % subject), content=content, author=self.user.username, subject=subject)
				page.put()
				self.list_cache(update=True)
			else:
				self.redirect('/_newpost')

		else:
			if not (old_page or content):
				return
			elif not old_page or old_page.content != content:
				page = Wiki.Wiki(parent = Wiki.Wiki.parent_key(path), content=content, author=self.user.username, subject=path[1:])
				page.put()
				self.list_cache(update=True)

		if path == '/_newpost' and subject != '':
			self.redirect('/%s' % subject)
		else:
			self.redirect(path)
