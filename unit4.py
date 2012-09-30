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
from access import AccessLoginHandler,AccessSignupHandler,AccessLogoutHandler,AccessWelcomeHandler

#ToDo change this to use the one in access.py        
class U4LoginHandler(AccessLoginHandler):
    def get(self):
        AccessLoginHandler.get(self)
    def post(self):
        redirect = '/unit3/blog/welcome'
        AccessLoginHandler.post(self,redirect)

class U4SignupHandler(AccessSignupHandler):
    def get(self):
        AccessSignupHandler.get(self)
    def post(self):
        redirect = '/unit3/blog/welcome'
        AccessSignupHandler.post(self,redirect)
                  
class U4LogoutHandler(AccessLogoutHandler):
    def get(self):
        redirect = '/unit3/blog/signup'
        AccessLogoutHandler.get(self,redirect)

class U4WelcomeHandler(AccessWelcomeHandler):
    def get(self):
        AccessWelcomeHandler.get(self)