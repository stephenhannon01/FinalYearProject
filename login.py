#!/usr/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage, escape
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie
import pymysql as db

form_data = FieldStorage()
beginning="""<section id = 'login'><form action = "login.py" method = "post">
                <label for = "username">User name: </label>
                <input type = "text" name = "username" id = "username"><br>
                <label for = "password">Password: </label>
                <input type = "password" name = "password" id = "password"><br>
                <input type = "submit" value = "Login">
            </form></section>"""
username = ''
result = ''
nav ="""
                   <ul id='nav'>
                       <li><a href="login.py">Login</a></li>
                       <li><a href="register.py">Register</a></li>
                   </ul>"""
if len(form_data) != 0:
    username = escape(form_data.getfirst('username', '').strip())
    password = escape(form_data.getfirst('password', '').strip())
    if not username or not password:
        result = '<p>Error: user name and password are required</p>'
    else:
        sha256_password = sha256(password.encode()).hexdigest()
        try:
            connection = db.connect('mysql.netsoc.co', 'visrec', 'hFfx3SJcsFUZV', 'visrec_users')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM users WHERE username = %s AND password = %s""", (username, sha256_password))
            if cursor.rowcount == 0:
                result = '<p>Error: incorrect user name or password</p>'
            else:

                ##########################################
                present = False
                userTable=cursor.fetchall()
                for row in userTable:
                    if row['username'] == username:
                        present = True
                ##########################################

                if present:
                    cookie= SimpleCookie()
                    sid = sha256(repr(time()).encode()).hexdigest()
                    cookie['sid'] = sid
                    session_store = open('sess_' + sid, writeback=True)
                    session_store['authenticated']=True
                    session_store['username'] = username
                    session_store.close()
                    nav ="""
                       <ul id='nav'>
                           <li><a href="rateMovie.py">Rate Movies</a></li>
                           <li><a href="getRecommendations.py">Get Recommendations</a></li>
                           <li><a href="logout.py">Log out</a></li>
                       </ul>"""
                    beginning='<p>Welcome back!</p>'
                else:
                    result = '<p>Error: incorrect user name or password</p>'
            cursor.close()
            connection.close()
        except (db.Error, IOError):
            result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print('Content-Type:text/html')
print()
print("""
    <!DOCTYPE html>
    <html lang = "en">
        <head>
            <link rel="stylesheet" type="text/css" href="http://visrec.netsoc.co/stylesheet.css">
            <title>Visual Recommender</title>
            %s
        </head>
            %s
            %s
        </body>
    </html>""" % (nav, beginning, result))
