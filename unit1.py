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
import webapp2
from tools import escape_html
   
months = ['January','February','March','April','May','June','July','August','September','October','November','December']

def valid_month(month):
   if month:
       cap = month.capitalize()
       if cap in months:
           return cap
   return None
def valid_day(day):
   if day.isdigit():
       d = int(day)
       if d>0 and d<31:
           return d
   return None
def valid_year(year):
   if year.isdigit():
       y = int(year)
       if y>1900 and y<2020:
           return y
   return None
   
def escape_html_old(s):
    s = s.replace('&','&amp;')
    s = s.replace('>','&gt;')
    s = s.replace('<','&lt;')
    s = s.replace('"','&quot;')
    return s

form = """
<form method="post">
   What is your birthday?
   <br>
	<label>Month
   	<input name="month" value="%(month)s">
   </label>
	<label>Day
		<input name="day" value="%(day)s">
   </label>
	<label>Year
		<input name="year" value="%(year)s">
   </label>
	<div style="color:red">%(error)s</div>
	<br>
   <br>
   <input type="submit">
</form>
"""          
class DateHandler(webapp2.RequestHandler):
    
    def write_form(self,error="",month="",day="",year=""):
        self.response.out.write(form%{"error":error,"month":escape_html(month),"day":escape_html(day),"year":escape_html(year)})
        
    def get(self):
        self.write_form()
        
    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')
        
        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)
        if not(month and day and year):
            self.write_form("That's an error!",user_month,user_day,user_year)
        else:
           self.redirect('/unit1/thanks')
           
class ThanksHandler(webapp2.RequestHandler):
     def get(self):
         self.response.out.write("Thanks! That's a totally valid date!")
         
class TestHandler(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text-plain'
        self.response.out.write(self.request)