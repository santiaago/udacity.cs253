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
import time
import logging
from datetime import datetime, timedelta
import cgi

def getDeltaTime(t):
    '''Returns the delta time between the given time t (in seconds) and now'''
    deltatime_sec = time.time() - t
    delta = datetime(1,1,1)+timedelta(seconds = deltatime_sec)
    return delta.time()

def getPrettyTime(t):
    ''' Returns a time t with pretty format
        we suppose var t format is %Y-%m-%d %H:%M:%S.%f'''
        
    t_struct = time.strptime(str(t),'%Y-%m-%d %H:%M:%S.%f')
    dt = datetime.fromtimestamp(time.mktime(t_struct))
    return dt.strftime('%A %B %d %H:%M:%S %Y')
    
#log helper
verbose = True
def log(msg):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("SAR:%s", str(msg))
#escape heler
def escape_html(s):
   return cgi.escape(s,quote = True)
   
#valid login helper
import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)
    
PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASSWORD_RE.match(password)
    
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)
#valid content
def valid_str(content):
    'returns True if string is not empty'
    if len(content)>0:
        return content
    return None