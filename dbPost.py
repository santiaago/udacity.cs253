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
from templateHelper import render_str
import time
def blog_key(name = 'default'):
      return db.Key.from_path('blogs', name)
      
def recent_posts():
    'return the top 10 posts'
    posts_and_time = memcache.get('posts_and_time')
    if posts_and_time is not None:
        return posts_and_time
    else:
        posts = db.GqlQuery("select * from Post order by created desc limit 10")
        cache_hit_time = time.time()
        posts_and_time = [posts,cache_hit_time]
        if not memcache.add('posts_and_time',posts_and_time):
            logging.error('Memcache set failed')
        return posts_and_time
def post_and_time_by_id(post_id):
    post_and_time = memcache.get('post_and_time'+str(post_id))
    if post_and_time is not None:
        return post_and_time
    else:
        post = db.Key.from_path('Post', int(post_id), parent=blog_key())
        cache_hit_time = time.time()
        post_and_time = [post,cache_hit_time]
        if not memcache.add('post_and_time'+str(post_id),post_and_time):
            logging.error('Memcache set failed')
        return post_and_time          
class Post(db.Model):
  subject = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)#current time when created

  def render(self):
      self._render_text = self.content.replace('\n', '<br>')
      return render_str("post.html", p = self)