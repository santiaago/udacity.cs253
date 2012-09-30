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
from crypto import make_pw_hash, valid_pw

def users_key(group = 'default'):
    return db.Key.from_path('users', group)
#ToDo move this to dbUser.py
class User(db.Model):
    name = db.StringProperty(required = True)    
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()
    
    @classmethod
    def by_id(cls,uid):
        return User.get_by_id(uid, parent = users_key())
    @classmethod
    def by_name(cls,name):
        u = User.all().filter('name =',name).get()
        return u
    @classmethod
    def register(cls,name,pw,email = None):
        pw_hash = make_pw_hash(name,pw)
        return User(parent = users_key(),name = name,pw_hash = pw_hash,email = email)
    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name,pw,u.pw_hash):
            return u