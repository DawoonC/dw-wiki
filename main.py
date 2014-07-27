#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

# URL Routing Table
#PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
PAGE_RE = r'(/(?:.+/?)*)'
app = webapp2.WSGIApplication(
	[(r'/_edit' + PAGE_RE, "handlers.editPage.EditPage"), 
	 (r'/signup', "handlers.signupPage.Register"), 
	 (r'/list', "handlers.listPage.ListPage"), 
	 (r'/login', "handlers.loginPage.LoginPage"), 
	 (r'/logout', "handlers.logoutPage.LogoutPage"),
	 (r'/flush', "handlers.flushCache.FlushCache"),
	 (r'/_history' + PAGE_RE, "handlers.historyPage.HistoryPage"),
	 (PAGE_RE, "handlers.wikiPage.WikiPage"),
	 ], debug=True)

