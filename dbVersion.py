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
from dbPage import Page

class Version(db.Model):
    ''' Version class
        a Page can have many versions of its content
        this is defined by the version_number property
    '''
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(required = True)
    version_number = db.IntegerProperty(required = True)
    page = db.ReferenceProperty(Page,collection_name = 'page_versions')
    def render(self):
        self._render_text = self.content.replace('\n','<br>')
        return self._render_text
    def render_time(self):
        return self.created.strftime('%A %B %d %H:%M:%S %Y')

def save_version(page):        
    '''save old version'''
    old_page_content = page.content
    old_page_version_number = page.version_number
    old_page_created = page.created
    Version(page = page, content = old_page_content, version_number = old_page_version_number, created = old_page_created).put()
    return None