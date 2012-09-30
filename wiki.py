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
from access import *
from templateHelper import renderHandler, render_str
from google.appengine.api import memcache
from dbPage import Page, get_page_and_time
from dbVersion import Version, save_version
from tools import getDeltaTime,log
from crypto import check_secure_val
import time

class WikiHandler(AccessWelcomeHandler):
    def get(self):
        AccessWelcomeHandler.get(self)

class WikiSignupHandler(AccessSignupHandler):
    def get(self):
        AccessSignupHandler.get(self)
    def post(self):
        redirect = '/wiki'
        AccessSignupHandler.post(self,redirect)
        
class WikiLoginHandler(AccessLoginHandler):
    def get(self):
        AccessLoginHandler.get(self)
    def post(self):
        redirect = '/wiki'
        AccessLoginHandler.post(self,redirect)

class WikiLogoutHandler(AccessLogoutHandler):
    def get(self):
        redirect = '/wiki/signup'
        AccessLogoutHandler.get(self,redirect)

class WikiEditHandler(renderHandler):
    '''
        User arrives to the WikiEdit Handler when:
            1 browsing for a page that does not exist.
              In that case open edit form to create new page.
            2 editing an existing page
    '''
    def write_form(self,content="",navigation=[]):
          self.render("edit.html", content = content,navigation = navigation)
          
    def get(self,url):
        uid = self.read_secure_cookie('user_id')
        u = uid and  User.by_id(int(uid))
        if u:
            #check if url already exists and show old contend to edit
            page_and_time = get_page_and_time(url)
            #get navigation bar
            uid = self.read_secure_cookie('user_id')
            user = uid and  User.by_id(int(uid))
            navigation = Navigation(user,url)
            
            if page_and_time is None:
                self.write_form('',navigation)
            else:
                page = page_and_time[0]
                self.write_form(page.content,navigation)
        else:
            self.redirect('/wiki/signup')
    def post(self,url):
        # check if page already exists if thats not the case create new page else update data
        page_and_time = get_page_and_time(url)
        page_content = self.request.get('content')
        page_url = url
        page = None
        if page_and_time is None: # new page!
            page = Page(key_name = page_url, content = page_content, version_number = 1)
            page.put() 
            # add it to memcache
            cache_hit_time = time.time()
            page_and_time = [page,cache_hit_time]
            if not memcache.add('page_and_time'+page_url,page_and_time):
                loggin.error('Memcache and failed')
        else: # edit old page
            page = page_and_time[0]
            # update new version
            page.content = page_content
            try:
                page.version_number = page.version_number + 1
            except:
                page.version_number = 1
            page.put()
            cache_hit_time = time.time()
            page_and_time_new = [page,cache_hit_time]
            if not memcache.set('page_and_time'+page_url,page_and_time_new):
                loggin.error('Memcache set failed')
        save_version(page)
        #redirect to new url
        self.redirect("/wiki%s" % str(page.key().name()))
    def read_secure_cookie(self,name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)
        
class WikiHistoryHandler(renderHandler):
    '''History handler'''
    def write_form(self,url = '',page_versions="",navigation=[]):
          self.render("history.html",current_url = url, page_versions = page_versions,navigation = navigation)
    def get(self,url):
        #check if url already exists and show list of versions
        page_and_time = get_page_and_time(url)
        #get navigation bar
        uid = self.read_secure_cookie('user_id')
        user = uid and  User.by_id(int(uid))
        navigation = Navigation(user,url)
        
        if page_and_time is None:
            self.write_form(url,'',navigation)
        else:
            page = page_and_time[0]
            self.write_form(url, page.page_versions,navigation)
    def post(self,url):
        return None
    def read_secure_cookie(self,name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)
        
def get_current_navigation(self,url):
    uid = self.read_secure_cookie('user_id')
    user = uid and  User.by_id(int(uid))
    navigation = Navigation(user,url)
    return navigation
    
class Navigation():
    nav_list = []
    def __init__(self, user,url=''):
        if user:
            self.nav_list = [['/wiki/_edit'+url,'edit'],['/wiki/_history'+url,'history'],['/wiki/logout','logout('+str(user.name)+')']]
        else:
            self.nav_list = [['/wiki/_history'+url,'history'],['/wiki/login','login'],['/wiki/signup','signup']]

    def render(self):
        return render_str("navigation.html", navigation = self.nav_list)
        
class WikiPageHandler(renderHandler):
    def read_secure_cookie(self,name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)
         
    def write_form(self,page_and_time,navigation):
        deltatime = getDeltaTime(page_and_time[1])
        self.render("page.html", page = page_and_time[0],cache_last_query = deltatime, navigation = navigation)
        
        
    def get(self,url):
        navigation = get_current_navigation(self,url)
        version = self.request.get('v')
        if version:
            #query version number
            page_and_time  = get_page_and_time(url)
            page = page_and_time[0]
            log(page_and_time[0].content)
            found_version = False
            for page_version in page.page_versions:
                if page_version.version_number == version:
                    page_and_time[0] = page_version
                    log(page_version.content)
                    found_version = True
                    break
            log(page_and_time[0].content)
            if not found_version:
                page_version = None
            self.write_form(page_and_time,navigation)
        else:
            page_and_time  = get_page_and_time(url)
            if page_and_time is None:
                # page does not exist redirect to create it!
                self.redirect("/wiki/_edit%s" % str(url)) 
            else:
                self.write_form(page_and_time,navigation)
