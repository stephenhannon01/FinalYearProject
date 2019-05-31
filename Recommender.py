#!/usr/bin/python3
import math
from MovieFileReader import *
from CustomerFileReader import *
from RatingsFileReader import *

class Recommender:
    
    def __init__(self):
        self.movies = MovieFileReader()
        self.customers = CustomerFileReader()
        self.ratings = RatingsFileReader()
        self.ratings.populate(self.movies, self.customers)
        self.noOfRecs = 5

    def getCustomerHashMap(self):
        return self.customers

    def printRec(self):
        for c in self.customers.getCustomers():
            self.recommend(c)

    def score(self, customer, movie):
        sum1=0.0
        sum2=0.0
        
        peopleWhoRatedTheMovies = self.movies.getPeopleRatingMovies(movie)
        for customerID in peopleWhoRatedTheMovies:
            w = self.weight(customer, customerID)
            sum1 += (w * self.customers.getRating(customerID, movie))
            sum2+= w

        if sum2==0.0:
            return 0
        else:
            return sum1/sum2
    
    '''def recommend(self, custID):
        c = customers.getCustomer(custID)
        bestRecommendation = None
        bestScore = -1.0
        for m in movies.getMovies():
            if not(c.hasRated(m.id()):
                s = score(custID, m.id())
                if s>bestScore:
                   bestScore = s
                   bestRecommendation = m'''


    def weight(self, c, x):
        m = self.customers.moviesInCommon(c, x)
        sum = 0.0
        if m is not None:  
            for movie in m:
                sum += math.pow(self.customers.getRating(c,movie) - customers.getRating(x, movie), 2)
        return 1/(1+math.sqrt(sum))

    def output(self, c, bestRecs, noOfRecs, bestRecScores):
        counter = 0
        outerList = []
        if bestRecs[0] != None:
            innerList=[]
            innerList.append(str(bestRecs[0].getName()))
            innerList.append(int(bestRecScores[0]))
            outerList.append(innerList)
            for movie in bestRecs:
                innerList=[]
                if movie!=None:
                    if not(bestRecs[0]==movie):
                        innerList.append(str(movie.getName()))
                        innerList.append(float(bestRecScores[counter]))
                        outerList.append(innerList)
                else:
                    break
                counter=counter+1
        return outerList

    def checkWhatPositionItShouldBeIn(self, s, bestRecScores):
        counter = 0
        while(counter<self.noOfRecs and counter<len(bestRecScores)):
            if bestRecScores==[]:
                break
            elif bestRecScores[counter]<s:
                break
            elif counter+1==len(bestRecScores) and len(bestRecScores)<self.noOfRecs:
                counter=counter+1
                break
            counter=counter+1
        return counter

    def putInPosition(self, position, bestRecs, m):
        newArray = []
        counter=0
        if len(bestRecs)==0:
            newArray.append(m)
        else:
            while(counter<position):
                newArray.append(bestRecs[counter])
                counter=counter+1
            if counter<self.noOfRecs:
                newArray.append(m)
            while counter<len(bestRecs) and counter+1<self.noOfRecs:
                newArray.append(bestRecs[counter])
                counter=counter+1
        return newArray

    def putInScore(self, position, bestRecScores, s):
        counter = 0
        newArray=[]
        while(counter<position):
            newArray.append(bestRecScores[counter])
            counter=counter+1
        if counter<self.noOfRecs:
            newArray.append(s)
        while counter<len(bestRecScores) and counter+1<self.noOfRecs:
            newArray.append(bestRecScores[counter])
            counter=counter+1
        return newArray

    def printRecsArray(self, movies):
        output="Array: "
        for movie in movies:
            if movie is not None:
                output = output + movie.getName()+ ", "
            else:
                output = output + "None, "
        #print(output)
        
    '''def turnToJSON(self, threedeearray):
        results = {}
        results['name']='Visualization Recommender'
        results['children']=[]
        #rows=cursor.execute("SELECT movie, score FROM customers")
        print (threedeearray)
        for row in threedeearray:
            movie = str(row[0])
            score = row[1]
            movieScore = {}
            movieScore['name']=movie
            movieScore['size']=score
            
            recommendation= {}
            recommendation['children']=[]
            recommendation['name']='recommendation'
            recommendation['children'].append(movieScore)
            
            results['children'].append(recommendation)

        return results'''
    
    def recommend(self, c):
        bestRecommendation = None
        bestRecScores = []
        bestRecs = []
        bestMovieScores = -1.0

        for m in self.movies.getMovies():
            if not c.hasRated(self.movies.getMovies()[m].ident()):
                s = self.score(c.id(), self.movies.getMovies()[m].ident())
                position = self.checkWhatPositionItShouldBeIn(s, bestRecScores)
                if position is not -1:
                    bestRecScores = self.putInScore(position, bestRecScores, s)
                    bestRecs = self.putInPosition(position, bestRecs, self.movies.getMovies()[m])

        output = self.output(c, bestRecs, self.noOfRecs, bestRecScores)
        return output
        #print (output)
