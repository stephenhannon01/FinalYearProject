#!/usr/bin/python3
from Recommender import *

def main(username):
    rec = Recommender()

    customerNameExists = False
    customerName = username
    customers = rec.getCustomerHashMap()
    for c in customers.getCustomers():
        if customers.getCustomers()[c].getName() == customerName:
            customerNameExists = True
            customer = customers.getCustomers()[c]
            break

    if customerNameExists == True:
        while customerNameExists == False:
            customerName = raw_input("Incorrect name, please enter your name:")
            customers = rec.getCustomerHashMap()
            for c in customers.getCustomers():
                if customers.getCustomers()[c].getName() == customerName:
                    customerNameExists = True
                    customer = customers.getCustomers()[c]
                    break

    rec.recommend(customer)

        
if __name__ == "__main__":
    main("Stephen")
