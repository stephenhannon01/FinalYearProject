#!/usr/bin/python3
from cgitb import enable
enable()
from cgi import FieldStorage, escape
from time import time
from os import environ
from shelve import open
from http.cookies import SimpleCookie
import pymysql as db

print('Content-Type: text/html')
print()
score=''
movieList=''
error=''
form = """<form action = "rateMovie.py" method = "post">
            <label for = "movie">Movie name: </label>
            <input type = "text" name = "movie" id = "movie"><br>
            <label for = "score">Score: </label>
            <input type = "text" name = "score" id = "score"><br>
            <input type = "submit" value = "Submit">
        </form>"""
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        sid = cookie['sid'].value
        session_store = open('sess_' + sid, writeback = False)
        if session_store.get('authenticated'):
            connection = db.connect('mysql.netsoc.co', 'visrec', 'hFfx3SJcsFUZV', 'visrec_users')
            cursor = connection.cursor(db.cursors.DictCursor)
            #get user id from database
            cursor.execute("""SELECT id FROM users where username = %s""",(str(session_store.get('username'))))
            userID=cursor.fetchone()['id']
            #get all movieIDs from ratings that he's rated
            cursor.execute("""SELECT movieID FROM ratings where custID = %s""",(userID))
            table=cursor.fetchall()
            #put it in set
            setOfRatedMovieIds=set()
            for row in table:
                setOfRatedMovieIds.add(row['movieID'])
            #turn movieIDs into movie names
            setOfRatedMovieNames = set()
            for movieId in set(setOfRatedMovieIds):
                cursor.execute("""SELECT name FROM movies where id=%s""",(movieId))
                output = cursor.fetchone()
                setOfRatedMovieNames.add(output['name'])
            #get all names from movies
            cursor.execute("""SELECT name FROM movies""")
            table=cursor.fetchall()
            setOfAllMovieNames=set()
            for row in table:
                setOfAllMovieNames.add(row['name'])
            #take one from the other and put it in movieList
            setOfUnratedMovieNames= setOfAllMovieNames - setOfRatedMovieNames
            movieList="<p>Here's a list of all of the movies you have not yet rated:"
            for movieName in setOfUnratedMovieNames:
                movieList=movieList+str(movieName)+"</br>"
            movieList=movieList+"</p>"
            
            
            ##############################################################
            form_data = FieldStorage()
            movie = ''
            score = ''
            if len(form_data) != 0:
                movie = escape(form_data.getfirst('movie', '').strip())
                score = escape(form_data.getfirst('score', '').strip())
                if not movie or not score:
                    error = '<p>Error: movie and score are required</p>'
                elif not score.isdigit():
                    error = '<p>Error: score must be a digit</p>'
                elif int(score)>5 or int(score)<0:
                    error = '<p>Error: score must be above 0 and equal to or below 5</p>'
                elif movie not in setOfUnratedMovieNames:
                    error = '<p>Error: movie must be in the list that is below</p>'
                else:
                    try:
                        cursor.execute("""SELECT id FROM movies where name = %s""",(movie))
                        output=cursor.fetchone()
                        movieID=output['id']
                        cursor.execute("""INSERT INTO ratings(custID, movieID, rating) VALUES (%s, %s, %s)""", (userID, movieID, score))
                            
                        connection.commit()
                        cursor.close()
                        error='Successfully scored!'
                    except (db.Error, IOError):
                            error = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'
            ###############################################
        session_store.close()
    else:
        form=''
        error="""<section id='error'>
                     <p>Please log in or register.</p>
		     <div id='parent'>
		         <div class='child'><a href="login.py">Login</a></div>
		         <div id="middle"></div>
		         <div class='child'><a href="register.py">Register</a></div>
		     </div>
		 </section>"""
except IOError:
    form = ''
    result = "<section id='error'><p>Sorry! We are experiencing problems at the moment. Please call back later.</p></section>"

print("""<!DOCTYPE html>
<html lang = "en">
    <head>
        <link rel="stylesheet" type="text/css" href="http://visrec.netsoc.co/stylesheet.css">
        <title>Visual Recommender</title>
        <ul id='nav'>
            <li><a href="rateMovie.py">Rate Movies</a></li>
            <li><a href="getRecommendations.py">Get Recommendations</a></li>
            <li><a href="logout.py">Log out</a></li>
        </ul>
    </head>
        %s
        %s
        <section id="movieList">%s</section>
    </body>
</html>""" % (form, error, movieList))
























    
    
