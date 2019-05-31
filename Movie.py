#!/usr/bin/python3
class Movie:
    
    def __init__(self, mid, name):
        self.mid=mid
        self.name=name
        self.ratedMe=set()

    def getName(self):
        return self.name

    def toString(self):
        return "id: "+str(self.mid)+" title: "+str(self.name)

    def customerRated(self, customerID):
        self.ratedMe.add(customerID)

    def getCustomersRated(self):
        return self.ratedMe

    def ident(self):
        return self.mid
