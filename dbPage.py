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
import time
from google.appengine.ext import db
from google.appengine.api import memcache

def get_page_and_time(page_url):
    ''' looks if it is in mem cache and return it if that is the case
        else if it exists get it from DB, store it in memcache and return it
        else return None'''
    page_and_time = memcache.get('page_and_time'+page_url)
    if page_and_time is not None:
        return page_and_time
    else:
        page = Page.get_by_key_name(page_url)
        if page is not None:
            cache_hit_time = time.time()
            page_and_time = [page,cache_hit_time]
            if not memcache.add('page_and_time'+page_url,page_and_time):
                loggin.error('Memcache set failed')
            return page_and_time
        else:
            return None
            
class Page(db.Model):
    ''' Page class
        content: the content of the page
        created: the date of creation
    '''
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    version_number = db.IntegerProperty(required = False)
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return self._render_text
    def render_time(self):
        return self.created.strftime('%b %d, %Y')
        
