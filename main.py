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
import re
from unit1 import *
from unit2 import *
from unit3 import *
from unit4 import *
from unit5 import *
from wiki import *
from testjinja2 import Jinja2Handler
   
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello Udacity!')

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/', MainHandler),
                                ('/unit1/date',DateHandler),
                                ('/unit1/thanks',ThanksHandler),
                                ('/unit2/rot13',Rot13Handler),
                                ('/unit2/welcome',WelcomeHandler),
                                ('/unit2/signup',SignupHandler),
                                ('/unit3/blog/?',BlogFront),
                                ('/unit3/blog/flush',U6FlushHandler),
                                ('/unit3/blog/newpost',NewPostHandler),
                                ('/jinja2',Jinja2Handler),
                                ('/unit3/blog/([0-9]+)', Permalink),
                                ('/unit3/blog/signup',U4SignupHandler),
                                ('/unit3/blog/welcome',U4WelcomeHandler),
                                ('/unit3/blog/login',U4LoginHandler),
                                ('/unit3/blog/logout',U4LogoutHandler),
                                ('/unit3/blog/\.json',U5JsonHandler),
                                ('/unit3/blog/(\d+)/?\.json',U5PermaJsonHandler),
                                ('/wiki/?',WikiHandler),
                                ('/wiki/signup',WikiSignupHandler),
                                ('/wiki/login',WikiLoginHandler),
                                ('/wiki/logout',WikiLogoutHandler),
                                ('/wiki/_history'+ PAGE_RE,WikiHistoryHandler),
                                ('/wiki/_edit'+ PAGE_RE,WikiEditHandler),
                                ('/wiki'+PAGE_RE,WikiPageHandler)],
                               #('/testform',TestHandler)],
                              debug=True)
