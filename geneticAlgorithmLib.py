from pyeasyga import pyeasyga
from random import *

rectValues = [0.5, 0.2, 0.1, 1.5, 0.5]

def randRect(): #creates random rectangle
    width = (randint(1, 101)-1)/100
    height = (randint(1, 101)-1)/100
    x = (randint(1, 101)-1)/100
    y = (randint(1, 101)-1)/100
    rect = [width, height, x, y]
    return rect

def randIndividual(recs): #creates random individual
    individual = []
    while recs>0:
        rect = randRect()
        individual.append(rect)
        recs = recs - 1
    return individual

def randPop(number): #creates random population
    recommendations = 5
    population = []

    while number>0:
        individual = []
        recs = recommendations
        individual = randIndividual(recs)
        population.append(individual)

        number = number -1

def fitness(ind, data):
    score = 0
    counter = 0
    maximumSize = 1
    for rect in individual:
        achievement = 0
        
        width = rect[0]
        height = rect[1]
        area = width*height

        x = rect[2]
        y = rect[3]
        

        #check to see if the area of the rectangle is the correct size
        #multiplied by 5 to increase the weight so that it'll be closer importance to overlapping
        
        if area>rectValues[counter]:
            achievement = (1/(area/rectValues[counter]))
        else:
            achievement = (area/rectValues[counter]) #a percentage of how close it is the what it needs to be

        #print('Correct size achievement: '+str(achievement))
        
        #check to see if the rectangle's area is inside perimeter
        #multiplied by 5 to increase the weight so that it'll be closer importance to overlapping
        ip = 0
        if width/2 + x > 1:
            #achievement = achievement + (1 - abs((width/2 + x) - 1)) #percentage of rectangle inside perimeter
            ip = 1 - abs((width/2 + x) - 1)

        if width/2 - x < 0:
            #achievement = achievement + (1 - abs(x - width/2))
            ip = achievement + (1 - abs(x - width/2))

        if height/2 + y > 1:
            #achievement = achievement + (1 - abs((height/2 + y) - 1))
            ip = achievement + (1 - abs((height/2 + y) - 1))

        if height/2 - x < 0:
            #achievement = achievement + (1 - abs(x - height/2))
            ip = achievement + (1 - abs(x - height/2))

        achievement = achievement + ip/4

        #print('Inside perimeter achievement: '+str(ip/4))
        
        
        #check to see if there are any overlaps between other rectangles
        #IMPORTANT: Y GOES FROM TOP TO BOTTOM
        ol = 0
        for rect in individual:
            if rect != individual[counter]:
                widthTwo = rect[0]
                heightTwo = rect[1]
                xTwo = rect[2]
                yTwo = rect[3]
                topRightTwo = [xTwo+(widthTwo/2),yTwo-(heightTwo/2)]
                botRightTwo = [xTwo+(widthTwo/2),yTwo+(heightTwo/2)]
                topLeftTwo = [xTwo-(widthTwo/2),yTwo-(heightTwo/2)]
                botLeftTwo = [xTwo-(widthTwo/2),yTwo+(heightTwo/2)]

                topRightOne = [x+(width/2),y-(height/2)]
                botRightOne = [x+(width/2),y+(height/2)]
                topLeftOne = [x-(width/2),y-(height/2)]
                botLeftOne = [x-(width/2),y+(height/2)]

                areaOfSecondRect = widthTwo*heightTwo

                if areaOfSecondRect == 0:
                    areaOfSecondRect = 0.01

                if botRightTwo[0]<=botRightOne[0] and botRightTwo[1]<=botRightOne[1] and botLeftTwo[0]>=botLeftOne[0] and topLeftTwo[1]>=topLeftOne[1]: #rect two is subset of rect one
                    ol = ol + 0
                elif topRightTwo[1]<topRightOne[1] and botRightTwo[1]>botRightOne[1] and botRightTwo[0]>botRightOne[0] and botLeftTwo[0]<botLeftOne[0] and botRightTwo[1]>topRightOne[1]: #rect two overlaps complete top half of rect one
                    heightOL = botLeftTwo[1] - topLeftOne[1]
                    widthOL = topRightOne[0] - topLeftOne[0]
                    areaOL = heightOL*widthOL
                    ol = ol + (1- areaOL/areaOfSecondRect)
                elif topRightTwo[1]<topRightOne[1] and botRightTwo[1]<botRightOne[1] and botRightTwo[0]<=botRightOne[0] and botLeftTwo[0]>=botLeftOne[0] and botRightTwo[1]>topRightOne[1]: #rect two overlaps a part of the top of rect one
                    heightOL = botLeftTwo[1] - topRightOne[1]
                    widthOL = botRightTwo[0] - botLeftTwo[0]
                    areaOL = heightOL*widthOL
                    ol = ol + (1- areaOL/areaOfSecondRect)
                elif topRightTwo[0]>topLeftOne[0] and topRightTwo[0]<topRightOne[0] and topLeftTwo[0]<topLeftOne[0] and topRightTwo[1]<topRightOne[1] and botRightTwo[1]>botRightOne[1]: #rect two overlaps complete left side of rect one
                    heightOL = botLeftOne[1] - topLeftOne[1]
                    widthOL = topRightTwo[0] - topLeftOne[0]
                    areaOL = heightOL*widthOL
                    ol = ol + (1- areaOL/areaOfSecondRect)
                elif topRightTwo[0]>topLeftOne[0] and topRightTwo[0]<topRightOne[0] and topLeftTwo[0]<topLeftOne[0] and topRightTwo[1]>=topRightOne[1] and botRightTwo[1]<=botRightOne[1]: #rect two overlaps a part of the left side of rect one
                    heightOL = botRightTwo[1] - topRightTwo[1]
                    widthOL = topRightTwo[0] - topLeftOne[0]
                    areaOL = heightOL*widthOL
                    ol = ol + (1- areaOL/areaOfSecondRect)
                elif topRightTwo[0]>topRightOne[0] and topRightTwo[1]>topRightOne[1] and topRightTwo[1]<botRightOne[1] and topLeftTwo[0]<topLeftOne[0] and botRightTwo[1]>botRightOne[1]: #rect two completely overlaps the bottom side of rect one
                    heightOL = botRightOne[1] - topRightTwo[1]
                    widthOL = botRightOne[0] - botLeftOne[0]
                    areaOL = heightOL*widthOL
                    ol = ol + (1- areaOL/areaOfSecondRect)
                elif topRightTwo[1]>topRightOne[1] and topRightTwo[1]<botRightOne[1] and botRightTwo[1]>botRightOne[1] and topRightTwo[0]<=topRightOne[0] and topLeftTwo[0]>=topLeftOne[0]: # rect two overlaps a part of the bottom side of rect one
                    heightOL = botLeftOne[1] - topRightTwo[1]
                    widthOL = topRightTwo[0] - topLeftTwo[0]
                    areaOL = heightOL*widthOL
                    ol = ol + (1- areaOL/areaOfSecondRect)
                elif topLeftTwo[0]>topLeftOne[0] and topLeftTwo[0]<topRightOne[0] and topRightTwo[0]>topRightOne[0] and topLeftTwo[1]<topLeftOne[1] and botLeftTwo[1]>botLeftOne[1]: #rect two overlaps completely the right side of rect one
                    heightOL = botRightOne[1] - topLeftOne[1]
                    widthOL = topRightOne[0] - topLeftTwo[0]
                    areaOL = heightOL*widthOL
                    ol = ol + (1- areaOL/areaOfSecondRect)
                elif topLeftTwo[0]>topLeftOne[0] and topLeftTwo[0]<topRightOne[0] and topRightTwo[0]>topRightOne[0] and topLeftTwo[1]>=topLeftOne[1] and botLeftTwo[1]<=botLeftOne[1]: #rect two overlaps a part of the right side of rect one
                    heightOL = botLeftTwo[1] - topLeftTwo[1]
                    widthOL = topRightOne[0] - topLeftTwo[0]
                    areaOL = heightOL*widthOL
                    ol = ol + (1- areaOL/areaOfSecondRect)
                elif topLeftTwo[1]>topLeftOne[1] and botLeftTwo[1]<botLeftOne[1] and topLeftTwo[0]<topLeftOne[0] and topRightTwo[0]>topRightOne[0]: #cross shape with rect two as horizontal
                    heightOL = botLeftTwo[1] - topLeftTwo[1]
                    widthOL = topRightOne[0] - topLeftOne[0]
                    areaOL = heightOL*widthOL
                    ol = ol + (1- areaOL/areaOfSecondRect)
                elif topLeftTwo[0]>topLeftOne[0] and topRightTwo[0]<topRightOne[0] and topRightTwo[1]<topRightOne[1] and botRightTwo[1]>botRightOne[1]: #cross shape with rect two as vertical
                    heightOL = botRightOne[1] - topRightOne[1]
                    widthOL = topRightTwo[0] - topLeftTwo[0]
                    areaOL = heightOL*widthOL
                    ol = ol + (1- areaOL/areaOfSecondRect)
                elif topRightTwo[0]>topLeftOne[0] and topRightTwo[0]<topRightOne[0] and topRightTwo[1]<topRightOne[1] and botRightTwo[1]>topLeftOne[1] and botRightTwo[1]<botLeftOne[1] and botLeftTwo[0]<topLeftOne[0]: #overlap on top left corner of rect one
                    heightOL = botRightTwo[1] - topLeftOne[1]
                    widthOL = topRightTwo[0] - topLeftOne[0]
                    areaOL = heightOL*widthOL
                    ol = ol + (1- areaOL/areaOfSecondRect)
                elif topLeftTwo[1]>topRightOne[1] and topLeftTwo[1]<botRightOne[1] and botRightTwo[1]>botRightOne[1] and topRightTwo[0]>botLeftOne[0] and topRightTwo[0]<botRightOne[0] and topLeftTwo[0]<topLeftOne[0]: #overlap on bot left corner of rect one
                    heightOL = botLeftOne[1] - topRightTwo[1]
                    widthOL = topRightTwo[0] - botLeftOne[0]
                    areaOL = heightOL*widthOL
                    ol = ol + (1- areaOL/areaOfSecondRect)
                elif topLeftTwo[1]>topLeftOne[1] and topLeftTwo[1]<botLeftOne[1] and topLeftTwo[0]>botLeftOne[0] and topLeftTwo[0]<botRightOne[0] and botRightTwo[1]>botRightOne[1] and topRightTwo[0]>topRightOne[0]: #overlap on the bottom right corner of rect one
                    heightOL = botRightOne[1] - topLeftTwo[1]
                    widthOL = topRightOne[0] - topLeftTwo[0]
                    areaOL = heightOL*widthOL
                    ol = ol + (1- areaOL/areaOfSecondRect)
                elif topLeftTwo[1]<botLeftOne[1] and botLeftTwo[1]>topRightOne[1] and botLeftTwo[1]<botRightOne[1] and botLeftTwo[0]>botLeftOne[0] and  botLeftTwo[0]<botRightOne[0] and topLeftTwo[1]<topRightOne[1] and topRightTwo[0]>topRightOne[0]: #overlaps one the top right corner of rect one
                    heightOL = botLeftTwo[1] - topRightOne[1]
                    widthOL = topRightOne[0] - topLeftTwo[0]
                    areaOL = heightOL*widthOL
                    ol = ol + (1- areaOL/areaOfSecondRect)
                else:
                    ol = ol + 1

        achievement = achievement + ol/5
        #print('Overlap achievement: '+str(ol/5))
        #print('')
                
        score = score + achievement**4
        counter = counter + 1

    return score

data = randPop(2500)
print('data')
ga = pyeasyga.GeneticAlgorithm(data)
print('data inputted')
#ga.create_individual = randIndividual(5)
ga.fitness_function = fitness
print('fitness set')
ga.run()
print (ga.best_individual())
