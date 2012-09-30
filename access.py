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
from dbUser import User
from templateHelper import renderHandler
from crypto import check_secure_val, make_secure_val
from tools import valid_username, valid_email, valid_password

class AccessLoginHandler(renderHandler):    
    ''' Login Handler'''
    def write_form(self,username="",error=""):
          self.render("login.html",username = username,error = error)
          
    def get(self):
        self.write_form()
        
    def post(self,sRedirectPath=''):
        username = self.request.get('username')
        password = self.request.get('password')
        
        user = User.login(username,password)
        if user:
            cookie_val = make_secure_val(str(user.key().id()))
            self.response.headers.add_header(
                 'Set-Cookie',
                 '%s=%s; Path=/' % ('user_id', cookie_val))
            self.redirect(sRedirectPath)
        else:
            msg = 'Invalid login'
            self.write_form('',msg)
            
class AccessLogoutHandler(webapp2.RequestHandler):
    def get(self,sRedirectPath):
        self.response.headers.add_header('Set-Cookie','user_id=; Path=/')
        self.redirect(sRedirectPath)
            
class AccessSignupHandler(renderHandler):
    
    def write_form(self,username="",password="",verify="",email="",errorUser="",errorPassword="",errorVerify="",errorEmail=""):
          self.render("signup.html",username = username,password = password, verify = verify,email = email,errorUser = errorUser,errorPassword = errorPassword,errorVerify = errorVerify,errorEmail = errorEmail)

    def get(self):
        self.write_form()
        
    def post(self,sRedirectPath=''):
        errorUser = errorPassword = errorVerify = errorEmail = ''
        
        username = self.request.get('username')
        password = self.request.get('password')
        verify  = self.request.get('verify')
        email = self.request.get('email')
        has_error = False
        if not valid_username(username):
            errorUser = 'That\'s not a valid username.'
            has_error = True
        if not valid_password(password):
            errorPassword = 'That wasn\'t a valid password.'
            has_error = True
        elif password != verify:
            errorVerify = 'Your passwords didn\'t match.'
            has_error = True

        if not valid_email(email):
            errorEmail = 'That\'s not a valid email.'
            has_error = True
        if has_error:
            password = ''
            verify = ''
            self.write_form(username,password,verify,email,errorUser,errorPassword,errorVerify,errorEmail)
        else:
            u = User.by_name(username)
            if u:
                errorUser = 'That user already exists'
                self.write_form(username,password,verify,email,errorUser,errorPassword,errorVerify,errorEmail)
            else:
                 u = User.register(username,password,email)
                 u.put()
                 cookie_val = make_secure_val(str(u.key().id()))
                 self.response.headers.add_header(
                     'Set-Cookie',
                     '%s=%s; Path=/' % ('user_id', cookie_val))
                 self.redirect(sRedirectPath)
                 
class AccessWelcomeHandler(webapp2.RequestHandler):
    
     def get(self,sRedirectPath=''):
         uid = self.read_secure_cookie('user_id')
         u = uid and  User.by_id(int(uid))
         if u:
             self.response.out.write('Welcome, %s'%str(u.name))
         elif len(sRedirectPath) > 0:
             self.redirect(sRedirectPath)
         else:
             self.response.out.write('Welcome')  
             
     def read_secure_cookie(self,name):
         cookie_val = self.request.cookies.get(name)
         return cookie_val and check_secure_val(cookie_val)