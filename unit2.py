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
from tools import escape_html, valid_username, valid_password, valid_email

htmlRot13 = """<!DOCTYPE html><html>
<head><title>Unit 2 Rot 13</title></head>
<body>
<h2>Enter some text to ROT13:</h2>
<form method="post">
<textarea name="text" style="height: 100px; width: 400px;">%(rot13)s</textarea><br>
<input type="submit">
</form>
</body>
</html>"""

class Rot13Handler(webapp2.RequestHandler):
    
    def write_form(self,rot13=""):
        self.response.out.write(htmlRot13%{"rot13":escape_html(rot13)})
        
    def get(self):
        self.write_form()
        
    def post(self):
        user_input = self.request.get('text')
        input_changed = user_input.encode('rot13')
        self.write_form(input_changed)
        
textsignup = '''<!DOCTYPE html><html>
<head><title>Sign Up</title><style type="text/css">.label {text-align: right}.error {color: red}</style></head>
<body>
<h2>Signup</h2>
<form method="post">
<table><tr><td class="label">Username</td><td><input type="text" name="username" value="%(username)s"></td><td class="error">%(errorUser)s</td></tr>
<tr><td class="label">Password</td><td><input type="password" name="password" value="%(password)s"></td><td class="error">%(errorPassword)s</td></tr
<tr><td class="label">Verify Password</td><td><input type="password" name="verify" value="%(verify)s"></td><td class="error">%(errorPasswordMatch)s</td></tr>
<tr><td class="label">Email (optional)</td><td><input type="text" name="email" value="%(email)s"></td><td class="error">%(errorEmail)s</td></tr>
</table>
<input type="submit">
</form>
</body>
</html>
'''
htmlWelcome='''
<!DOCTYPE html><html>
<head>
<title>Unit 2 Signup</title>
</head>
<body>
<h2>Welcome, %(username)s!</h2>
</body>
</html>
'''   
class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username= self.request.get('username')
        self.response.out.write(htmlWelcome%{'username':username})

class SignupHandler(webapp2.RequestHandler):
    def write_form(self,username="",password="",verify="",email="",errorUser="",errorPassword="",errorVerify="",errorEmail=""):
        self.response.out.write(textsignup%{
                                        "username":escape_html(username),
                                        "errorUser":escape_html(errorUser),
                                        "password":escape_html(password),
                                        "errorPassword":escape_html(errorPassword),
                                        "verify":escape_html(verify),
                                        "errorPasswordMatch":escape_html(errorVerify),
                                        "email":escape_html(email),
                                        "errorEmail":escape_html(errorEmail)})
    def get(self):
        self.write_form()
    def post(self):
        errorUser = errorPassword = errorVerify = errorEmail = ''
        
        username = self.request.get('username')
        password = self.request.get('password')
        verify  = self.request.get('verify')
        email = self.request.get('email')
        
        if not (valid_username(username) and valid_password(password) and (password == verify) and valid_email(email)):
            if not valid_username(username):
                errorUser = 'That\'s not a valid username.'
            if not valid_password(password):
                errorPassword = 'That wasn\'t a valid password.'
            if password != verify:
                errorVerify = 'Your passwords didn\'t match.'
            if not valid_email(email):
                errorEmail = 'That\'s not a valid email.'
                
            password = ''
            verify = ''
            self.write_form(username,password,verify,email,errorUser,errorPassword,errorVerify,errorEmail)
        else:
            self.redirect("/unit2/welcome?username="+str(username))