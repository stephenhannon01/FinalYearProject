#!/usr/bin/python3
from Movie import *
import pymysql as db

class MovieFileReader:

    def __init__(self):
        self.movies = {}
        #self.readMoviesFile(filename)
        self.readTable()

    '''def readMoviesFile(self, filename):
        lineArray=[]
        with open(filename, "r") as f:
            for line in f.readlines():
                lineArray=line.strip().split('|')
                try:
                    movieID = int(lineArray[0])
                    movieName = lineArray[1]
                    newMovie = Movie(movieID, movieName)
                    self.movies[movieID] = newMovie
                except ValueError:
                    print 'Error in movie file format'
        f.close()'''

    def readTable(self):
        try:
            connection = db.connect('mysql.netsoc.co', 'visrec', 'hFfx3SJcsFUZV', 'visrec_users')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM movies""")
            moviesTable = cursor.fetchall()
            
            for row in moviesTable:
                movieID = row['id']
                movieName = row['name']
                newMovie = Movie(movieID, movieName)
                self.movies[movieID] = newMovie
                
            cursor.close()
            connection.close()
        except (db.Error, IOError):
            print('Error: reading movies tables.')

    def getPeopleRatingMovies(self, movieID):
        return self.movies[movieID].getCustomersRated()

    def getMovies(self):
        return self.movies

    def customerHasRated(self, customerID, movieID):
        #print(self.movies)
        return self.movies[movieID].customerRated(customerID)
