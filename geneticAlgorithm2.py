from random import *
import math
import statistics

#def dist(x, y, a, b):return math.sqrt( (x-a)**2 + (y-b)**2 )

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

    return population

def fitness(population, rectValues): #determines fitness of each individual in the population
    fitList = []
    for individual in population:
        fitList.append(fitnessScore(individual, rectValues))

    return fitList
'''
def rankList(lst): #output list best being biggest rank
    sortedList = sorted(lst)
    ranksList = []
    lstPosition = 0
    print('started')
    for member in lst:
        lstPosition = 0
        for sortedMember in reversed(sortedList):
            if member == sortedMember:
                ranksList.append(lstPosition)
            lstPosition = lstPosition + 1
    
    print('done')
    return ranksList
'''
'''
def invertFitList(fitList):
    biggestScore = 0
    smallestScore = 1000
    for score in fitList:
        if score>biggestScore:
            biggestScore = score
            
    newFitList = []
    for score in fitList:
        newFitList.append(int((biggestScore - score) + 1)) #smallest score becomes biggest score

    return newFitList

'''

def fitnessScore(individual, rectValues):
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
        if area>rectValues[counter]:
            #punishment =((area - rectValues[counter])*10)
            #achievement = (maximumSize - (area - rectValues[counter]))
            #achievement = 1-(area/rectValues[counter]-1) #a percentage of how close it is the what it needs to be
            achievement = 1/(area/rectValues[counter])
            #print("area: "+str(area))
            #print("rectValues[counter]: "+str(rectValues[counter]))
            #print("area>rectValues: "+str(achievement))
            #print()
        else:
            #punishment =((rectValues[counter] - area)*10)
            #achievement =(maximumSize - (rectValues[counter] - area))
            achievement = area/rectValues[counter] #a percentage of how close it is the what it needs to be
            #print("area>rectValues else: "+str(achievement))

        #score = score + punishment
        
        #check to see if the rectangle's area is inside perimeter
        if width/2 + x > 1:
            achievement = achievement + (1 - abs((width/2 + x) - 1)) #percentage of rectangle inside perimeter
            #score = score + ((width/2 + x) - 1)*10 # how much its out of the perimeter on the right side
            #print("width/2 + x > 1: "+str(achievement))

        if width/2 - x < 0:
            achievement = achievement + (1 - abs(x - width/2))
            #score = score + (x - width/2)*10 # how much its out of the perimeter on the left side
            #print("width/2 - x < 0: "+str(achievement))

        if height/2 + y > 1:
            achievement = achievement + (1 - abs((height/2 + y) - 1))
            #score = score + ((height/2 + y) - 1)*10 # how much its out of the perimeter on the bottom
            #print("height/2 + y > 1: "+str(achievement))

        if height/2 - x < 0:
            achievement = achievement + (1 - abs(x - height/2))
            #score = score + (x - height/2)*10 #how much its out of the perimeter on the top
            #print("height/2 - x < 0: "+str(achievement))
        
        
        #check to see if there are any overlaps between other rectangles
        #IMPORTANT: Y GOES FROM TOP TO BOTTOM
        
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
                '''
                    
                if botRightOne[0]<botRightTwo[0] and botLeftOne[0]>botLeftTwo[0] and botLeftOne[1]<botLeftTwo[1] and topLeftOne[0]#rect1 is subset of rect2
                else:
                #topleft overlap
                    if botRightTwo[0]>topLeftOne[0] and botRightTwo[1]>topLeftOne[1] and topLeftTwo[0]<topLeftOne[0]:
                        widthOfOL = botRightTwo[0] - topLeftOne[0]
                        print(botRightTwo[0])
                        print(topLeftOne[0])
                        print()
                        heightOfOL = botRightTwo[1] - topLeftOne[1]
                        areaOfOL = widthOfOL*heightOfOL
                        print("topleft: "+str((areaOfOL/areaOfSecondRect)))
                        achievement = achievement + (1 - areaOfOL/areaOfSecondRect) #percentage of area that isn't overlapping
                        #score = score + areaOfOL*10


                    #topright overlap
                    if botLeftTwo[0]<topRightOne[0] and botLeftTwo[1]>topRightOne[1]:
                        widthOfOL =  topRightOne[0] - botLeftTwo[0]
                        heightOfOL = botLeftTwo[1] - topRightOne[1]
                        #print("botLeftTwo[1]: "+str(botLeftTwo[1]))
                        #print("topRightOne[1]: "+str(topRightOne[1]))
                        #print("widthOfOL: "+str(widthOfOL))
                        #print("heightOfOL: "+str(heightOfOL))
                        areaOfOL = widthOfOL*heightOfOL
                        #print("areaOfOL/areaOfSecondRect: "+str(areaOfOL/areaOfSecondRect))
                        #print("areaOfSecondRect: "+str(areaOfSecondRect))
                        #print("areaOfOL: "+str(areaOfOL))
                        achievement = achievement + (1 - areaOfOL/areaOfSecondRect)
                        #print("topright: "+str(achievement))
                        #score = score + areaOfOL*10
                        
                    #botleft overlap
                    if topRightTwo[0]>botLeftOne[0] and topRightTwo[1]<botLeftOne[1]:
                        widthOfOL = topRightTwo[0] - botLeftOne[0]
                        heightOfOL = botLeftOne[1] - topRightTwo[1]
                        #print("topRightTwo[1: "+str(topRightTwo[1]))
                        #print("botLeftOne[1]: "+str(botLeftOne[1]))
                        #print("widthOfOL: "+str(widthOfOL))
                        #print("heightOfOL: "+str(heightOfOL))
                        areaOfOL = widthOfOL*heightOfOL
                        #print("areaOfOL/areaOfSecondRect: "+str(areaOfOL/areaOfSecondRect))
                        #print("areaOfSecondRect: "+str(areaOfSecondRect))
                        #print("areaOfOL: "+str(areaOfOL))
                        achievement = achievement + (1 - areaOfOL/areaOfSecondRect)
                        #print("botleft: "+str(achievement))
                        #score = score + areaOfOL*10

                    #botright overlap
                    if topLeftTwo[0]<botRightOne[0] and topLeftTwo[1]<botRightOne[1]:
                        widthOfOL = botRightOne[0] - topLeftTwo[0]
                        heightOfOL = botRightOne[1] - topLeftTwo[1]
                        areaOfOL = widthOfOL*heightOfOL
                        achievement = achievement + (1 - areaOfOL/areaOfSecondRect)
                        #print("botright: "+str(achievement))
                        #score = score + areaOfOL*10
                        #score = score + achievement*10
                    #print('')
                    '''
                #print('achievement: '+str(achievement))
                if botRightTwo[0]<botRightOne[0] and botRightTwo[1]<botRightOne[1] and botLeftTwo[0]>botLeftOne[0] and topLeftTwo[1]>topLeftOne[1]: #rect two is subset of rect one
                    achievement = achievement + 0
                elif topRightTwo[1]<topRightOne[1] and botRightTwo[1]>botRightOne[1] and botRightTwo[0]>botRightOne[0] and botLeftTwo[0]<botLeftOne[0] and botRightTwo[1]>topRightOne[1]: #rect two overlaps complete top half of rect one
                    heightOL = botLeftTwo[1] - topLeftOne[1]
                    widthOL = topRightOne[0] - topLeftOne[0]
                    areaOL = heightOL*widthOL
                    achievement = achievement + (1- areaOL/areaOfSecondRect)
                elif topRightTwo[1]<topRightOne[1] and botRightTwo[1]<botRightOne[1] and botRightTwo[0]<botRightOne[0] and botLeftTwo[0]>botLeftOne[0] and botRightTwo[1]>topRightOne[1]: #rect two overlaps a part of the top of rect one
                    heightOL = botLeftTwo[1] - topRightOne[1]
                    widthOL = botRightTwo[0] - botLeftTwo[0]
                    areaOL = heightOL*widthOL
                    achievement = achievement + (1- areaOL/areaOfSecondRect)
                elif topRightTwo[0]>topLeftOne[0] and topRightTwo[0]<topRightOne[0] and topLeftTwo[0]<topLeftOne[0] and topRightTwo[1]<topRightOne[1] and botRightTwo[1]>botRightOne[1]: #rect two overlaps complete left side of rect one
                    heightOL = botLeftOne[1] - topLeftOne[1]
                    #print('heightOL: '+str(heightOL))
                    widthOL = topRightTwo[0] - topLeftOne[0]
                    #print('widthOL: '+str(widthOL))
                    areaOL = heightOL*widthOL
                    achievement = achievement + (1- areaOL/areaOfSecondRect)
                elif topRightTwo[0]>topLeftOne[0] and topRightTwo[0]<topRightOne[0] and topLeftTwo[0]<topLeftOne[0] and topRightTwo[1]>topRightOne[1] and botRightTwo[1]<botRightOne[1]: #rect two overlaps a part of the left side of rect one
                    heightOL = botRightTwo[1] - topRightTwo[1]
                    widthOL = topRightTwo[0] - topLeftOne[0]
                    areaOL = heightOL*widthOL
                    #print('achievement: '+str(1- areaOL/areaOfSecondRect))
                    achievement = achievement + (1- areaOL/areaOfSecondRect)
                elif topRightTwo[0]>topRightOne[0] and topRightTwo[1]>topRightOne[1] and topRightTwo[1]<botRightOne[1] and topLeftTwo[0]<topLeftOne[0] and botRightTwo[1]>botRightOne[1]: #rect two completely overlaps the bottom side of rect one
                    heightOL = botRightOne[1] - topRightTwo[1]
                    widthOL = botRightOne[0] - botLeftOne[0]
                    areaOL = heightOL*widthOL
                    achievement = achievement + (1- areaOL/areaOfSecondRect)
                elif topRightTwo[1]>topRightOne[1] and topRightTwo[1]<botRightOne[1] and botRightTwo[1]>botRightOne[1] and topRightTwo[0]<topRightOne[0] and topLeftTwo[0]>topLeftOne[0]: # rect two overlaps a part of the bottom side of rect one
                    heightOL = botLeftOne[1] - topRightTwo[1]
                    widthOL = topRightTwo[0] - topLeftTwo[0]
                    areaOL = heightOL*widthOL
                    achievement = achievement + (1- areaOL/areaOfSecondRect)
                elif topLeftTwo[0]>topLeftOne[0] and topLeftTwo[0]<topRightOne[0] and topRightTwo[0]>topRightOne[0] and topLeftTwo[1]<topLeftOne[1] and botLeftTwo[1]>botLeftOne[1]: #rect two overlaps completely the right side of rect one
                    heightOL = botRightOne[1] - topLeftOne[1]
                    widthOL = topRightOne[0] - topLeftTwo[0]
                    areaOL = heightOL*widthOL
                    achievement = achievement + (1- areaOL/areaOfSecondRect)
                elif topLeftTwo[0]>topLeftOne[0] and topLeftTwo[0]<topRightOne[0] and topRightTwo[0]>topRightOne[0] and topLeftTwo[1]>topLeftOne[1] and botLeftTwo[1]<botLeftOne[1]: #rect two overlaps a part of the right side of rect one
                    heightOL = botLeftTwo[1] - topLeftTwo[1]
                    widthOL = topRightOne[0] - topLeftTwo[0]
                    areaOL = heightOL*widthOL
                    achievement = achievement + (1- areaOL/areaOfSecondRect)
                elif topRightTwo[0]>topLeftOne[0] and topRightTwo[0]<topRightOne[0] and topRightTwo[1]<topRightOne[1] and botRightTwo[1]>topLeftOne[1] and botRightTwo[1]<botLeftOne[1] and botLeftTwo[0]<topLeftOne[0]: #overlap on top left corner of rect one
                    heightOL = botRightTwo[1] - topLeftOne[1]
                    widthOL = topRightTwo[0] - topLeftOne[0]
                    areaOL = heightOL*widthOL
                    achievement = achievement + (1- areaOL/areaOfSecondRect)
                elif topLeftTwo[1]>topRightOne[1] and topLeftTwo[1]<botRightOne[1] and botRightTwo[1]>botRightOne[1] and topRightTwo[0]>botLeftOne[0] and topRightTwo[0]<botRightOne[0] and topLeftTwo[0]<topLeftOne[0]: #overlap on bot left corner of rect one
                    heightOL = botLeftOne[1] - topRightTwo[1]
                    widthOL = topRightTwo[0] - botLeftOne[0]
                    areaOL = heightOL*widthOL
                    achievement = achievement + (1- areaOL/areaOfSecondRect)
                elif topLeftTwo[1]>topLeftOne[1] and topLeftTwo[1]<botLeftOne[1] and topLeftTwo[0]>botLeftOne[0] and topLeftTwo[0]<botRightOne[0] and botRightTwo[1]>botRightOne[1] and topRightTwo[0]>topRightOne[0]: #overlap on the bottom right corner of rect one
                    heightOL = botRightOne[1] - topLeftTwo[1]
                    widthOL = topRightOne[0] - topLeftTwo[0]
                    areaOL = heightOL*widthOL
                    achievement = achievement + (1- areaOL/areaOfSecondRect)
                elif topLeftTwo[1]<botLeftOne[1] and botLeftTwo[1]>topRightOne[1] and botLeftTwo[1]<botRightOne[1] and botLeftTwo[0]>botLeftOne[0] and  botLeftTwo[0]<botRightOne[0] and topLeftTwo[1]<topRightOne[1] and topRightTwo[0]>topRightOne[0]: #overlaps one the top right corner of rect one
                    heightOL = botLeftTwo[1] - topRightOne[1]
                    widthOL = topRightOne[0] - topLeftTwo[0]
                    areaOL = heightOL*widthOL
                    #print('heightOL: '+str(heightOL))
                    #print('widthOL: '+str(widthOL))
                    #print('achievement: '+str(1- areaOL/areaOfSecondRect))
                    achievement = achievement + (1- areaOL/areaOfSecondRect)
                else:
                    achievement = achievement + 1
                
        score = score + achievement*10
        counter = counter + 1

    return score

def elongatedPopList(population, fitList):  #makes copies of each individual in accordance with its fitness score
    elongatedList = []
    popLen = len(population)
    counter = 0
    while counter<popLen:
        counterTwo = fitList[counter]
        while counterTwo>0:
            elongatedList.append(population[counter])
            counterTwo = counterTwo -1
        
        counter = counter + 1

    return elongatedList
    
def copyX(population, ePL, copyProportion, fitnessList):
    totalCopies = len(population)*copyProportion
    amount = totalCopies
    copied = []

    while amount > 0:
        choice = randint(1, len(ePL))-1
        while ePL[choice] in copied: #makes sure the same person isn't copied more than once
            choice = randint(1, len(ePL))-1
            
        copied.append(ePL[choice])

        amount = amount - 1 
    return copied

def crossover(population, ePL, crossoverProportion, fitnessList):
    totalOffspring = len(population)*crossoverProportion
    #5 rectangles
    #4 features of each rectangle
    numOfRec = 5
    
    offSpring = []
    while totalOffspring > 0:
        random = randint(1, len(ePL))-1
        individualOne = ePL[random]
        random = randint(1, len(ePL))-1
        while ePL[random] == individualOne: #making sure two different parents are chosen
            random = randint(1, len(ePL))-1
        individualTwo = ePL[random]
        
        chosenRect = randint(1, numOfRec)-1
        if chosenRect == numOfRec-1:
            secondChosenRect = 0
        else:
            secondChosenRect = chosenRect+1
        
        individualOne[chosenRect] = individualTwo[chosenRect]
        individualOne[secondChosenRect] = individualTwo[secondChosenRect]

        offSpring.append(individualOne)
        totalOffspring = totalOffspring - 1

    return offSpring
'''
def mutate(population, mutationRate): #randomly selects a few rectangles and replaces them with a new random rectangle
    rectangles = 5
    features = 4
    totalMutation = len(population)*mutationRate
    counter = 0
    while counter < totalMutation:
        randRect = randint(1, rectangles)-1
        randFeature = randint(1, features)-1
        individual = randint(1, len(population))-1
        population[individual][randRect][randFeature] = (randint(1, 101)-1)/100
        counter = counter + 1

    return population
'''
def mutate(population, mutationRate): #randomly selects a few rectangles and replaces them with a new random rectangle
    rectangles = 5
    features = 4
    
    totalMutation = len(population)*mutationRate
    counter = 0
    while counter < totalMutation:
        randRect = randint(1, rectangles)-1
        randFeature = randint(1, features)-1
        
        position = randint(1, len(population))-1
        randInd = randIndividual(5)
        population[position][randRect][randFeature] = (randint(1, 101)-1)/100
        population[position] = randInd
        counter = counter + 1

    return population

def geneticAlgorithm(individualNo, crossoverProportion, mutationRate, rectValues):
    copy = 0
    generations = 50
    k = 0
    population = randPop(individualNo)
    fitnessList = fitness(population, rectValues)
    #findBest(population, fitnessList)
    while generations > 0:
        print('Generation: '+str(generations))
        print("Average: "+str(sum(fitnessList)/len(fitnessList)))
        print("Median: "+str(statistics.median(fitnessList)))
        findBest(population, fitnessList)
        #invertScores = invertFitList(fitnessList) #gives the best score the biggest score
        ePL = elongatedPopList(population, fitnessList) #makes copies of each individual in accordance with its fitness score
        copy = copyX(population, ePL, 1-crossoverProportion, fitnessList)
        offspring = crossover(population, ePL, crossoverProportion, fitnessList)
        population = copy + offspring
        population = mutate(population, mutationRate)
        fitnessList = fitness(population, rectValues)
        
        generations = generations - 1

    return findBest(population, fitnessList)
    

def findBest(population, fitnessList):
    bestPosition = 0
    bestScore = 0
    counter = 0
    worstScore = 100000
    
    for score in fitnessList:
        if score<worstScore:
            worstScore = score
        if score>bestScore:
            bestScore = score
            bestPosition = counter
        counter = counter + 1
    print('bestScore: '+str(bestScore))
    print('worstScore: '+str(worstScore))
    print(population[bestPosition])
    print()

    return population[bestPosition]

rectValues = [0.5, 0.2, 0.1, 1.5, 0.5]
geneticInfo = geneticAlgorithm(5000, 0.3, 0.05, rectValues)

##################################################################
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

rects=[]
print('1')

for rect in geneticInfo:
    width = rect[0]
    height = rect[1]
    x = rect[2]
    y = rect[3]
    topRight = [x+(width/2),y-(height/2)]
    botRight = [x+(width/2),y+(height/2)]
    topLeft = [x-(width/2),y-(height/2)]
    botLeft = [x-(width/2),y+(height/2)]
    rects.append([topRight, botRight, topLeft, botLeft])

verts1 = [
    (rects[0][3][0], rects[0][3][1]), # left, bottom
    (rects[0][2][0], rects[0][2][1]), # left, top
    (rects[0][0][0], rects[0][0][1]), # right, top
    (rects[0][1][0], rects[0][1][1]), # right, bottom
    (0, 0), # ignored
    ]
verts2 = [
    (rects[1][3][0], rects[1][3][1]), # left, bottom
    (rects[1][2][0], rects[1][2][1]), # left, top
    (rects[1][0][0], rects[1][0][1]), # right, top
    (rects[1][1][0], rects[1][1][1]), # right, bottom
    (0, 0), # ignored
    ]
verts3 = [
    (rects[2][3][0], rects[2][3][1]), # left, bottom
    (rects[2][2][0], rects[2][2][1]), # left, top
    (rects[2][0][0], rects[2][0][1]), # right, top
    (rects[2][1][0], rects[2][1][1]), # right, bottom
    (0, 0), # ignored
    ]
verts4 = [
    (rects[3][3][0], rects[3][3][1]), # left, bottom
    (rects[3][2][0], rects[3][2][1]), # left, top
    (rects[3][0][0], rects[3][0][1]), # right, top
    (rects[3][1][0], rects[3][1][1]), # right, bottom
    (0, 0), # ignored
    ]
verts5 = [
    (rects[4][3][0], rects[4][3][1]), # left, bottom
    (rects[4][2][0], rects[4][2][1]), # left, top
    (rects[4][0][0], rects[4][0][1]), # right, top
    (rects[4][1][0], rects[4][1][1]), # right, bottom
    (0, 0), # ignored
    ]

codes = [Path.MOVETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.CLOSEPOLY,
         ]

path1 = Path(verts1, codes)
path2 = Path(verts2, codes)
path3 = Path(verts3, codes)
path4 = Path(verts4, codes)
path5 = Path(verts5, codes)

fig = plt.figure()
ax = fig.add_subplot(111)
patch1 = patches.PathPatch(path1, facecolor='orange', lw=2)
patch2 = patches.PathPatch(path2, facecolor='blue', lw=2)
patch3 = patches.PathPatch(path3, facecolor='red', lw=2)
patch4 = patches.PathPatch(path4, facecolor='green', lw=2)
patch5 = patches.PathPatch(path5, facecolor='yellow', lw=2)
ax.add_patch(patch1)
ax.add_patch(patch2)
ax.add_patch(patch3)
ax.add_patch(patch4)
ax.add_patch(patch5)
ax.set_xlim(0,1)
ax.set_ylim(0,1)
plt.show()
