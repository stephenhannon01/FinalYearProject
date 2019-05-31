#!/usr/bin/python3
from geneticAlgorithm import *
from htmlRetrieve import *
import urllib
from cgitb import enable
enable()
from cgi import FieldStorage, escape
from time import time
from os import environ
from shelve import open
from http.cookies import SimpleCookie
import pymysql as db
from dataFrame import *
from Recommender import *
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from random import randint
PersonalhighestRatedMovieRow=""
PersonalLowestRatedMovieRow=""

def euc(x,xprime):return np.sqrt(np.sum((x-xprime)**2))

def binaryVersion(movie):
    movieSimInfo=[movie[4], movie[1], movie[5]]
    if movie[2] == 'action' or movie[3] == 'action':
        movieSimInfo.append(True)
    else:
        movieSimInfo.append(False)
    if movie[2] == 'animation' or movie[3] == 'animation':
        movieSimInfo.append(True)
    else:
        movieSimInfo.append(False)
    if movie[2] == 'biography' or movie[3] == 'biography':
        movieSimInfo.append(True)
    else:
        movieSimInfo.append(False)
    if movie[2] == 'drama' or movie[3] == 'drama':
        movieSimInfo.append(True)
    else:
        movieSimInfo.append(False)
    if movie[2] == 'horror' or movie[3] == 'horror':
        movieSimInfo.append(True)
    else:
        movieSimInfo.append(False)
    if movie[2] == 'mystery' or movie[3] == 'mystery':
        movieSimInfo.append(True)
    else:
        movieSimInfo.append(False)
    if movie[2] == 'sci-fi' or movie[3] == 'sci-fi':
        movieSimInfo.append(True)
    else:
        movieSimInfo.append(False)
    if movie[2] == 'comedy' or movie[3] == 'comedy':
        movieSimInfo.append(True)
    else:
        movieSimInfo.append(False)

    return movieSimInfo
        
    
X=[0]
m=[]
recommendations=5
features=12
while recommendations>=0:
    print(recommendations)
    n=[]
    while features>=0:
        n.append(recommendations)
        features=features-1
    m.append(n)
    m.append(n)
    m.append(n)
    m.append(n)
    m.append(n)
    m.append(n)
    recommendations=recommendations-1
    print(recommendations)
print(recommendations)
#order - descending strength, ascending strength, alphabetical, weakest in middle, strongest in middle, genres (favourite genre first)
#groupby - genre
#colour - poster, age rating, random, genre
#size - recommender rating, imdb rating
beginning="""<form action="getRecommendations.py" method="post">
                <h1>Treemap Preferences</h1>
                <label for="color">Colour</label>
                <section id='colourForm'>
                    <select id="color" name="color">
                        <option value="empty">No Preference</option>
                        <option value="age rating color">Age Rating</option>
                        <option value="name">Distinct</option>
                        <option value="primary_genre">Genre</option>
                    </select>
                </section>
                <label for="size">Size</label>
                <section id='sizeForm'>
                    <select id="size" name="size">
                        <option value="empty">No Preference</option>
                        <option value="value">Recommender Rating</option>
                        <option value="imdb_rating">IMDB Rating</option>
                    </select>
                </section>
                <label for="order">Order</label>
                <section id='orderForm'>
                    <select id="order" name="order">
                        <option value="empty">No Preference</option>
                        <option value="desc">Descending rating</option>
                        <option value="asc">Ascending rating</option>
                        <option value="strongMiddle">Strongest Rating in middle</option>
                        <option value="weakMiddle">Weakest Rating in middle</option>
                        <option value="simPersBest">Similarity of Personal Best Rated Movie in Descending</option>
                        <option value="simPersWorst">Similarity of Personal Worst Rated Movie in Descending</option>
                        <option value="genre">Genre</option>
                        <option value="alphabetical">Alphabetical</option>
                        <option value="genetic">Genetic</option>
                    </select>
                </section>
                <label for="htmlinfo">Pop-up Window Info</label>
                <section id='htmlinfo'>
                    <select id="htmlinfo" name="htmlinfo">
                        <option value="general">General Information</option>
                        <option value="ageratinginfo">Age Rating Information</option>
                        <option value="btsinfo">Images</option>
                        <option value="criticinfo">Critic Review</option>
                        <option value="castcrewinfo">Cast & Crew Information</option>
                        <option value="awardsinfo">Awards Reviews</option>
                    </select>
                </section>
                <input type="submit" value="Submit" />
            </form>"""

print('Content-Type: text/html')
print()
error=''
color=''
treemap=""
sortedList=""
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
            form = FieldStorage()
            if form.getvalue('color') and form.getvalue('size') and form.getvalue('order') and form.getvalue('htmlinfo'):
                color = form.getvalue('color')
                size = form.getvalue('size')
                order = form.getvalue('order')
                htmlInfo = form.getvalue('htmlinfo')
                
                rec = Recommender()
                customerName = session_store.get('username')
                customers = rec.getCustomerHashMap()
                for c in customers.getCustomers():
                    if customers.getCustomers()[c].getName() == customerName:
                        customer = customers.getCustomers()[c]
                        break
                        
                r=rec.recommend(customer)
                m=[]
                allMovieInfo=[]

                totalValue = 0

                for recommendation in r:
                    totalValue = totalValue + recommendation[1]

                imdbRatingTotal = 0

                valueTotal = 0
                
                for recommendation in r:
                    cursor.execute("""SELECT name, imdb_rating, primary_genre, secondary_genre, age_rating, synopsis, imdb_link, image_name FROM movies where name = %s""",(recommendation[0]))
                    movieDict=cursor.fetchone()
                    allMovieInfo.append(movieDict)
                    ageColour=""
                    if movieDict['age_rating'] == 0:
                        ageColour="#27ce14"
                    elif movieDict['age_rating'] <= 7:
                        ageColour="#86db1e"
                    elif movieDict['age_rating'] <= 12:
                        ageColour="#ddaf18"
                    elif movieDict['age_rating'] <= 15:
                        ageColour="#e0541d"
                    elif movieDict['age_rating'] <= 18:
                        ageColour="#bc2727"

                    imdbRatingTotal = imdbRatingTotal + (movieDict['imdb_rating']**3)

                    
                            
                    movieList=[movieDict['name'],movieDict['imdb_rating']**3,movieDict['primary_genre'],movieDict['secondary_genre'],(recommendation[1]/totalValue)**3, movieDict['age_rating'], ageColour]
                    m.append(movieList)

                    valueTotal = valueTotal + movieList[4]

                for movieList in m:
                    movieList[1] = movieList[1]/imdbRatingTotal
                    movieList[4] = movieList[4]/valueTotal
                    

                #order - descending strength, ascending strength, alphabetical, weakest in middle, strongest in middle, genres (favourite genre first)
                #groupby - genre
                #color - poster, age rating, random, genre
                #size - recommender rating, imdb rating

                #recommender is in order of highest to lowest
                #imdb size is m[1]

                if form.getvalue('general'):
                   general = 1
                else:
                   general = 0

                if form.getvalue('ageratinginfo'):
                   ageratinginfo = 1
                else:
                   ageratinginfo = 0

                if form.getvalue('purchase'):
                   purchase = 1
                else:
                   purchase = 0

                if form.getvalue('criticreview'):
                   criticreview = 1
                else:
                   criticreview = 0

                if form.getvalue('castandcrew'):
                   castandcrew = 1
                else:
                   castandcrew = 0

                if form.getvalue('awards'):
                   awards = 1
                else:
                   awards = 0

                if order == "empty":
                    orderList=['asc', 'desc', 'strongMiddle', 'weakMiddle', 'genre', 'alphabetical', 'simPersBest', 'simPersWorst']
                    random=randint(0, 7)
                    order=orderList[random]

                if size == "empty":
                    orderList=['imdb_rating', 'value']
                    random=randint(0, 1)
                    size=orderList[random]

                if color == "empty":
                    orderList=['age rating color', 'name', 'primary_genre']
                    random=randint(0, 2)
                    color=orderList[random]
                    
                if order == "asc":
                    if size == "imdb_rating":
                        sortedList=[]
                        for movie in m:
                            sortedList.append(movie[1])
                        sortedList.sort()
                        
                        for movie in m:
                            counter2 = 0
                            for element in sortedList:
                                if movie[1] == element:
                                    movie.append(len(sortedList)-counter2)#because the movie that should be the first will be in index 0 but the order puts the biggest in front
                                    break
                                counter2=counter2+1

                    elif size == "value": #already ordered by recommender ratings
                        counter=0
                        for movie in m:
                            movie.append(counter)
                            counter=counter+1
                
                elif order == "desc":
                    if size == "imdb_rating":
                        sortedList=[]
                        for movie in m:
                            sortedList.append(movie[1])
                        sortedList.sort()
                        for movie in m:
                            counter2 = 0
                            for element in sortedList:
                                if movie[1] == element:
                                    movie.append(counter2)#because the biggest movie will be in index 0 of sortedList but the order puts the biggest in front
                                    break
                                counter2=counter2+1
                    elif size == "value": #already ordered by recommender ratings
                        counter=len(m)
                        for movie in m:
                            movie.append(counter)
                            counter=counter-1
                            
                elif order == "strongMiddle":
                    if size == "imdb_rating":
                        sortedList=[]
                        for movie in m:
                            sortedList.append(movie[1])
                        sortedList.sort()
                        for movie in m:
                            if movie[1]==sortedList[0]:
                                movie.append(3)
                            elif movie[1]==sortedList[1]:
                                movie.append(2)
                            elif movie[1]==sortedList[2]:
                                movie.append(4)
                            elif movie[1]==sortedList[3]:
                                movie.append(1)
                            else:
                                movie.append(5)
                    elif size == "value": #already ordered by recommender ratings
                        listO=[3,2,4,1,5]
                        counter=0
                        for movie in m:
                            movie.append(listO[counter])
                            counter=counter+1
                            
                elif order == "weakMiddle":
                    if size == "imdb_rating":
                        sortedList=[]
                        for movie in m:
                            sortedList.append(movie[1])
                        sortedList.sort()
                        for movie in m:
                            if movie[1]==sortedList[0]:
                                movie.append(1)
                            elif movie[1]==sortedList[1]:
                                movie.append(5)
                            elif movie[1]==sortedList[2]:
                                movie.append(2)
                            elif movie[1]==sortedList[3]:
                                movie.append(4)
                            else:
                                movie.append(3)
                    elif size == "value": #already ordered by recommender ratings
                        listO=[1,5,2,4,3]
                        counter=0
                        for movie in m:
                            movie.append(listO[counter])
                            counter=counter+1

                elif order == "genre":
                    genres={}
                    counter=0
                    for movie in m:
                        if movie[4] not in genres:
                            genres[movie[4]]=counter
                            movie.append(counter)
                            counter=counter+1
                        else:
                            movie.append(genres[movie[4]])

                elif order == "alphabetical":
                    sortedList=[]
                    for movie in m:
                        sortedList.append(movie[0])
                    sortedList.sort()
                    for movie in m:
                        counter2 = 0
                        for element in sortedList:
                            if movie[0] == element:
                                movie.append(len(sortedList)-counter2)
                                break
                            counter2=counter2+1
                            
                elif order == "simPersBest" or order == "simPersWorst":
                    cursor.execute("""SELECT id FROM users where username = %s""",(str(session_store.get('username'))))
                    userID=cursor.fetchone()['id']
                
                    if order == "simPersBest":
                        cursor.execute("""SELECT movieID FROM ratings where custID = %s ORDER BY rating DESC""",(userID))
                        personalhighestRatedMovieRow=cursor.fetchone()
                        cursor.execute("""SELECT * FROM movies where id = %s""" % (personalhighestRatedMovieRow['movieID']))
                        personal=cursor.fetchone()
                    else:
                        cursor.execute("""SELECT movieID FROM ratings where custID = %s ORDER BY rating ASC""",(userID))
                        personalLowestRatedMovieRow=cursor.fetchone()
                        cursor.execute("""SELECT * FROM movies where id = %s""" % (personalLowestRatedMovieRow['movieID']))
                        personal=cursor.fetchone()

                    personal=[personal['name'],personal['imdb_rating'],personal['primary_genre'],personal['secondary_genre'],0,personal['age_rating']]
                    dataFrameInfo=[]
                    
                    for movie in m:
                        #action, animation, biography, drama, horror, mystery, sci-fi, comedy
                        dataFrameInfo.append(binaryVersion(movie))
                    dataFrameInfo.append(binaryVersion(personal))

                    #action, animation, biography, drama, horror, mystery, sci-fi, comedy
                    df = pd.DataFrame(dataFrameInfo,columns=['recommender_rating', 'imdb_rating', 'age_rating', 'action', 'animation', 'biography', 'drama', 'horror', 'mystery', 'sci-fi', 'comedy'])
                    numeric_features = ["imdb_rating", "recommender_rating", "age_rating"]
                    nominal_features = ["action", "animation", "biography", "drama", "horror", "mystery", "sci-fi", "comedy"]
                    # Create the pipelines
                    numeric_pipeline=Pipeline([("selector",DataFrameSelector(numeric_features,"float64")),("scaler",MinMaxScaler())])
                    nominal_pipeline=Pipeline([("selector",DataFrameSelector(nominal_features))])
                    pipeline=Pipeline([("union",FeatureUnion([("numeric_pipeline",numeric_pipeline),("nominal_pipelines",nominal_pipeline)]))])
                    pipeline.fit(df)
                    X = pipeline.transform(df)

                    counter=0
                    for movie in X:
                        m[counter].append(euc(movie,X[len(X)-1])) #appended as the order
                        counter=counter+1
                        if counter is 5:
                            break

                elif order == "genetic":
                    '''
                    yCurrent = 0
                    mCopy = []
                    for movieList in m:
                        movieList.append(0) #order doesn't matter
                        movieList.append(yCurrent + movieList[4]/2) #x
                        movieList.append(0.5)#y
                        yCurrent = yCurrent + movieList[4]
                        movieList.append(movieList[4])#width
                        movieList.append(1)#height

                        mCopy.append(movieList)

                    m = mCopy
                    '''
                    rectValues = []
                    for movieList in m:
                        rectValues.append(movieList[4])
                        
                    geneticInfo = geneticAlgorithm(10000, 0.5, 0.01, rectValues)
                    counter = 0

                    mCopy = []
                    for movieList in m:
                        movieList.append(0)
                        movieList.append(geneticInfo[counter][2])#x
                        movieList.append(geneticInfo[counter][3])#y
                        movieList.append(geneticInfo[counter][0])#width
                        movieList.append(geneticInfo[counter][1])#height
                        counter = counter + 1
                        mCopy.append(movieList)

                    m = mCopy

                counter=0
                while counter<5:
                    for movies in allMovieInfo:
                        if movies['name'] is m[counter][0]:
                            #print(movies['name'])
                            image = movies['image_name']
                            if htmlInfo == 'general':
                                
                                html=generalHtml(movies['imdb_link'])
                                html = "<section id='container'><img src='http://visrec.netsoc.co/"+image+"'><section id='text'>"+html+"</section></section>"
                                
                            elif htmlInfo == 'ageratinginfo':
                                html=htmlParental(movies['imdb_link'])
                                html = "<section id='container'><img src='http://visrec.netsoc.co/"+image+"'><section id='text'>"+html+"</section></section>"
                                
                            elif htmlInfo == 'btsinfo':
                                html=htmlImages(movies['imdb_link'])
                                html = "<section id='images'>"+html+"</section>"
                                
                            else:
                                html = 'Work in progress.'

                            if 'Predators' in movies['name']:
                                html = ''

                            m[counter].append(html)
                            #m[counter].append(movies['imdb_link'])
                            break
                    counter=counter+1

                treemap="""var visualization = d3plus.viz()
                    .container("#viz")  
                    .data(sample_data)
                    .type("tree_map")
                    .id(["name"])
                    .color("%s")
                    .size("%s")
                    .legend(false)
                    .ui([
                      {
                        "method" : "size",
                        "value"  : [ "value" , "imdb_rating" ]
                      },
                      {
                        "method" : "color",
                        "value"  : [ "name" , "age rating" ]
                      }
                    ])
                    .tooltip({
                        "curtain":{"color": "black"},
                        "share":false,
                        "html": function(node) {
                            if(node=="%s"){
                                return "%s";
                            }else if(node=="%s"){
                                return "%s";
                            }else if(node=="%s"){
                                return "%s";
                            }else if(node=="%s"){
                                return "%s";
                            }else{
                                return "%s";
                            }
                    }}
                    )
                    .format({
                      "text": function(text, params) {
                        if (text === "value") {
                          return "Recommender Rating";
                        }
                        else if(text === "Imdb_Rating"){
                          return "IMDB Rating"
                        }
                        else {
                          return d3plus.string.title(text, params);
                        } 
                      },
                      "number": function(number, params) {
                        
                        var formatted = d3plus.number.format(number, params);
                        
                        if (params.key === "value") {
                          return Math.round(Math.cbrt(formatted) * 100) / 100+"/5";
                        }
                        else if(params.key === "imdb_rating"){
                            return formatted+"/10";
                        }
                        else{
                          return formatted;
                        }
                        
                      }
                    })
                    .draw()""" %(color, size,
                                #name       image
                                m[0][0],   m[0][12],
                                m[1][0],   m[1][12],
                                m[2][0],   m[2][12],
                                m[3][0],   m[3][12],
                                           m[4][12])

                
                beginning=""                
            else:
                subject = "Not set"
            ###############################################
        session_store.close()
    else:
        beginning=''
        error="""<section id='error'>
                     <p>Please log in or register.</p>
		     <div id='parent'>
		         <div class='child'><a href="login.py">Login</a></div>
		         <div id="middle"></div>
		         <div class='child'><a href="register.py">Register</a></div>
		     </div>
		 </section>"""
except IOError:
    error = "<section id='error'><p>Sorry! We are experiencing problems at the moment. Please call back later.</p></section>"

print("""<!DOCTYPE html>
<html lang = "en">
<meta charset="utf-8">
    <head>
        <link rel="stylesheet" type="text/css" href="http://visrec.netsoc.co/stylesheet.css">
        <title>Visual Recommender</title>
        <script src="http://feynman.netsoc.co:6969/d3.js"></script>
        <script src="http://feynman.netsoc.co:6969/d3plus.js"></script>
        <ul id='nav'>
            <li><a href="rateMovie.py">Rate Movies</a></li>
            <li><a href="getRecommendations.py">Get Recommendations</a></li>
            <li><a href="logout.py">Log out</a></li>
        </ul>
    </head>
    <body>
        %s
        %s
        <div id="viz"></div>
        
        <script>
            var sample_data = [
                {"primary_genre": "%s", "secondary_genre": "%s", "value": %s, "name": "%s", "imdb_rating": %s, "age rating": %s, "order": %s, "age rating color":"%s", "xGraph": %s, "yGraph": %s, "widthGraph": %s, "heightGraph": %s},
                {"primary_genre": "%s", "secondary_genre": "%s", "value": %s, "name": "%s", "imdb_rating": %s, "age rating": %s, "order": %s, "age rating color":"%s", "xGraph": %s, "yGraph": %s, "widthGraph": %s, "heightGraph": %s},
                {"primary_genre": "%s", "secondary_genre": "%s", "value": %s, "name": "%s", "imdb_rating": %s, "age rating": %s, "order": %s, "age rating color":"%s", "xGraph": %s, "yGraph": %s, "widthGraph": %s, "heightGraph": %s},
                {"primary_genre": "%s", "secondary_genre": "%s", "value": %s, "name": "%s", "imdb_rating": %s, "age rating": %s, "order": %s, "age rating color":"%s", "xGraph": %s, "yGraph": %s, "widthGraph": %s, "heightGraph": %s},
                {"primary_genre": "%s", "secondary_genre": "%s", "value": %s, "name": "%s", "imdb_rating": %s, "age rating": %s, "order": %s, "age rating color":"%s", "xGraph": %s, "yGraph": %s, "widthGraph": %s, "heightGraph": %s},
                {"primary_genre": "", "secondary_genre": "", "value": 0, "name": "lowest", "imdb_rating": 0, "age rating": 0, "order": 0, "age rating color":"#214"},
                {"primary_genre": "", "secondary_genre": "", "value": 0, "name": "highest", "imdb rating": 0, "age rating": 18, "order": 0, "age rating color":"#274"}        
              ]
         %s   
        </script>
    </body>
    %s
    %s
</html>""" % (beginning, error,
              #prim genre   sec genre       value       name        imdb rating     age rating      order       ageColour      x         y          width      height
              m[0][2],      m[0][3],        m[0][4],    m[0][0],    m[0][1],        m[0][5],        m[0][7],    m[0][6],    m[0][8],    m[0][9],    m[0][10],    m[0][11],
              m[1][2],      m[1][3],        m[1][4],    m[1][0],    m[1][1],        m[1][5],        m[1][7],    m[1][6],    m[1][8],    m[1][9],    m[1][10],    m[1][11],
              m[2][2],      m[2][3],        m[2][4],    m[2][0],    m[2][1],        m[2][5],        m[2][7],    m[2][6],    m[2][8],    m[2][9],    m[2][10],    m[2][11],
              m[3][2],      m[3][3],        m[3][4],    m[3][0],    m[3][1],        m[3][5],        m[3][7],    m[3][6],    m[3][8],    m[3][9],    m[3][10],    m[3][11],
              m[4][2],      m[4][3],        m[4][4],    m[4][0],    m[4][1],        m[4][5],        m[4][7],    m[4][6],    m[4][8],    m[4][9],    m[4][10],    m[4][11],
              treemap, PersonalhighestRatedMovieRow, PersonalLowestRatedMovieRow))


















    
    
