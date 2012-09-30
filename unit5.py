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
from templateHelper import renderHandler
import json

class U5PermaJsonHandler(renderHandler):
    def get(self,post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        time_fmt = '%c'
        data = {"content":post.content,
                "subject":post.subject,
                "created":post.created.strftime(time_fmt)}
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(json.dumps(data))

class U5JsonHandler(webapp2.RequestHandler):
    def get(self):
        posts = db.GqlQuery("select * from Post order by created desc limit 10")
        page = []
        time_fmt = '%c'
        for post in posts:
            data = {"content":post.content,
                    "subject":post.subject,
                    "created":post.created.strftime(time_fmt)}
            page.append(data)
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(json.dumps(page))