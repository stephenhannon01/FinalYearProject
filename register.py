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

username = ''
result = ''
beginning ="""<form action = "register.py" method = "post">
            <label for = "username">User name: </label>
            <input type = "text" name = "username" id = "username"><br>
            <label for = "password1">Password: </label>
            <input type = "password" name = "password1" id = "password1"><br>
            <label for = "password2">Re-enter password: </label>
            <input type = "password" name = "password2" id = "password2"><br>
            <input type = "submit" value = "Register">
        </form>"""
nav ="""<ul id='nav'>
        <li><a href="login.py">Login</a></li>
        <li><a href="register.py">Register</a></li>
    </ul>"""
if len(form_data) != 0:
    username = escape(form_data.getfirst('username', '').strip())
    password1 = escape(form_data.getfirst('password1', '').strip())
    password2 =  escape(form_data.getfirst('password2', '').strip())
    if not username or not password1 or not password2:
        result = '<section id="error"><p>Error: user name and passwords are required</p></section>'
    elif password1 != password2:
        result = '<section id="error"><p>Error: passwords must be equal</p></section>'
    elif len(username) > 51:
        result = '<section id="error"><p>Error: Please reduce the length of your username.</p></section>'
    else:
        try:
            connection = db.connect('mysql.netsoc.co', 'visrec', 'hFfx3SJcsFUZV', 'visrec_users')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM users WHERE username = %s""", (username))
            if cursor.rowcount > 0:
                result = '<p>Error: user name already taken</p>'
            else:
                sha256_password = sha256(password1.encode()).hexdigest()
                cursor.execute("""INSERT INTO users (username, password) VALUES (%s, %s) """, (username, sha256_password))
                connection.commit()
                cursor.close()
                cookie= SimpleCookie()
                sid = sha256(repr(time()).encode()).hexdigest()
                cookie['sid'] = sid
                session_store = open('sess_' + sid, writeback=True)
                session_store['authenticated']=True
                session_store['username'] = username
                session_store.close()
                beginning ='<p>Thanks for joining Visual Recommender</p>'
                nav = """
                    <ul id='nav'>
                        <li><a href="rateMovie.py">Rate Movies</a></li>
                        <li><a href="getRecommendations.py">Get Recommendations</a></li>
                        <li><a href="logout.py">Log out</a></li>
                    </ul>"""
                #print(cookie)
        except (db.Error, IOError) as e:
                #print(e)
                #result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'
                result = '<p>'+str(e)+'</p>'

print('Content-Type:text/html')
print()
print("""<!DOCTYPE html>
    <html lang = "en">
        <head>
            <link rel="stylesheet" type="text/css" href="stylesheet.css">
            <title>Visual Recommender</title>
            %s
        </head>
        <body>
            %s
            %s
        </body>
    </html>""" % (nav, result, beginning))
























                       
