#!/usr/bin/python3
class Customer:
    def __init__(self, id, name):
        self.name = name
        self.custID = id
        self.movieRatings = {}
        self.moviesRated = set()

    def getName(self):
        return self.name

    def toString(self):
        return self.custID +": "+self.name;

    def hasRated(self, movieID):
        return movieID in self.movieRatings

    def rateMovie(self, movieID, rating):
        self.movieRatings[movieID]=rating
        self.moviesRated.add(movieID)

    def getRating(self, movieID):
        return self.movieRatings[movieID]

    def getMoviesRated(self):
        return self.moviesRated

    def id(self):
        return self.custID
