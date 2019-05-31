#!/usr/bin/python3
from Customer import *
import pymysql as db

class CustomerFileReader:

    def __init__(self):
        self.customers = {}
        #self.readCustomerFile(filename)
        self.readTable()
        

    '''def readCustomerFile(self, filename):
        lineArray=[]
        with open(filename) as f:
            for line in f:
                lineArray=line.strip().split('|')
                #print("LineArray: "+str(lineArray))
                try:
                    custID = int(lineArray[0])
                    customerName = lineArray[1]
                    newCustomer = Customer(custID, customerName)
                    self.customers[custID] = newCustomer
                except ValueError:
                    print 'Error in customer file format'
        f.close()'''

    def readTable(self):
        try:
            connection = db.connect('mysql.netsoc.co', 'visrec', 'hFfx3SJcsFUZV', 'visrec_users')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM users""")
            usersTable = cursor.fetchall()
            
            for row in usersTable:
                custID = row['id']
                customerName = row['username']
                newCustomer = Customer(custID, customerName)
                self.customers[custID] = newCustomer
                
            cursor.close()
            connection.close()
        except (db.Error, IOError):
            print('Error: reading movies tables.')

    def moviesInCommon(self, cus1, cus2):
        cus2Movies = self.customers[cus2].getMoviesRated()
        common=set()
        for m1 in self.customers[cus1].getMoviesRated():
            if m1 in cus2Movies:
                common.add(m1)

    def getCustomer(self, custID):
        return self.customers[custID]

    def getCustomers(self):
        return self.customers

    def rateMovie(self, custID, movieID, rating):
        self.customers[custID].rateMovie(movieID, rating)

    def getRating(self, custID, movieID):
        return self.customers[custID].getRating(movieID)
        
        
