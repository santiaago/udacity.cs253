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
import os
import webapp2
from google.appengine.ext import db
from google.appengine.api import memcache
from tools import escape_html, valid_str
from templateHelper import renderHandler, render_str
from dbPost import Post, recent_posts, post_and_time_by_id, blog_key
import time

class BlogFront(renderHandler):
    def get(self):
        posts = recent_posts()
        cache_hit_time = posts[1]
        # OR posts = Post.all().order('-created')
        self.render('blog.html', posts = posts[0],cache_last_hit = round(time.time() - cache_hit_time))

class NewPostHandler(renderHandler):
  def write_form(self,error="",subject="",content=""):
      self.render("newpost.html", error = error,subject = subject, content = content)

  def get(self):
      self.write_form()
  def post(self):
      user_subject = self.request.get('subject')
      user_content = self.request.get('content')

      subject = valid_str(user_subject)
      content = valid_str(user_content)
      if not(subject and content):
          self.write_form("We need to set both a subject and some content",user_subject,user_content)
      else:
          p = Post(parent = blog_key(), subject = user_subject,content = user_content)
          p.put()
          #redirect to permalink
          self.redirect("/unit3/blog/%s" % str(p.key().id()))
class Permalink(renderHandler):
  def get(self, post_id):
      #key = db.Key.from_path('Post', int(post_id), parent=blog_key())
      key  = post_and_time_by_id(post_id)
      post = db.get(key[0])
      cache_hit_time = key[1]
      if not post:
          self.error(404)
          return
      self.render("permalink.html", post = post,cache_last_hit = round(time.time() - cache_hit_time))
class U6FlushHandler(webapp2.RequestHandler):
    def get(self):
        #flush all caches
        memcache.flush_all()
        self.redirect('/unit3/blog')      