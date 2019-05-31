#!/usr/bin/python3
from cgitb import enable
enable()

from os import environ
from shelve import open
from http.cookies import SimpleCookie

print('Content-Type: text/html')
print()

result = ''
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if not http_cookie_header:
        result = '<p>You are already logged out</p>'
    else:
        cookie.load(http_cookie_header)
        sid = cookie['sid'].value
        session_store = open('sess_' + sid, writeback = True)
        session_store['authenticated'] = False
        session_store.close()
        result = """
           <p>You are now logged out. Thanks for using Visual Recommender.</p>"""
except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print("""
   <!DOCTYPE html>
   <html lang = "en">
       <head>
           <link rel="stylesheet" type="text/css" href="http://visrec.netsoc.co/stylesheet.css">
           <title>Visual Recommender</title>
           <ul id='nav'>
		   <li><a href="login.py">Login</a></li>
		   <li><a href="register.py">Register</a></li>
	   </ul>
       </head>
       <body>
           %s
       </body>
   </html>""" % (result))
