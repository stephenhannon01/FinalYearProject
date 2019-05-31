#!/usr/bin/python3
from http.cookies import SimpleCookie
import pymysql as db
class RatingsFileReader:

    def __init__(self):
        self.ratings = []
        #self.readRatingsFile(filename)
        self.readTable()

    '''def readRatingsFile(self, filename):
        lineArray=[]
        with open(filename, "r") as f:
            for line in f.readlines():
                lineArray=line.strip().split('|')
                try:
                    ratingfirst = []
                    for x in range(0, 3):
                        ratingfirst.append(int(lineArray[x]))
                    self.ratings.append(ratingfirst)
                except ValueError:
                    print 'Error in ratings file format'
        f.close()'''

    def readTable(self):
        try:
            connection = db.connect('mysql.netsoc.co', 'visrec', 'hFfx3SJcsFUZV', 'visrec_users')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM ratings""")
            ratingsTable = cursor.fetchall()

            #ratingfirst = []
            lineArray = []
            
            for row in ratingsTable:
                lineArray=[row['custID'], row['movieID'], row['rating']]
                self.ratings.append(lineArray)

            cursor.close()
            connection.close()
            
        except (db.Error, IOError):
            print('Error: reading ratings tables.')



    def populate(self, movies, customers):
        for r in self.ratings:
            customers.rateMovie(r[0],r[1],r[2]) 
            movies.customerHasRated(r[0],r[1])
