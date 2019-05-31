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
    worstScore = 10000
    for individual in population:
        score = fitnessScore(individual, rectValues)
        fitList.append(score)
        if score<worstScore:
            worstScore = score

    difference = worstScore - 1
    newFitList = []
    totalFitScore = 0
    for score in fitList:
        totalFitScore = totalFitScore+(score)
        #newFitList.append(score-difference) #scales all scores down by the worst score minus one
        newFitList.append(score)

    return [totalFitScore,newFitList]
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

def chooseRandomIndividual(fitnessList, totalFitScore):
    counter = 0
    randPosition = randint(1, int(totalFitScore))
    for score in fitnessList:
        if score>=randPosition:
            break
        randPosition = randPosition - score
        counter = counter+1
    #print('chooseRandomIndividual: '+str(counter))
    return counter

'''def tournament(noInTournament, fitnessList, totalFitScore):
    tournament = []
    counter = noInTournament
    while counter>0:
        tournament.append(chooseRandomIndividual(fitnessList, totalFitScore))
        counter = counter-1

    best = 0
    second = 0
    third = 0
    
    for person in tournament:
        if fitnessList[person]>fitnessList[best]:
            second = best
            best = person
        elif fitnessList[person]>fitnessList[second]:
            third = second
            second = person
        elif fitnessList[person]>fitnessList[third]:
            third = person
    
    print('best: '+str(fitnessList[best]))
    print('second: '+str(fitnessList[second]))
    for score in tournament:
        print('tournament: '+str(fitnessList[score]))

    print('')
    #print('')
    #print(str(fitnessList[best])+' at '+str(best))
    
    return [best, second, third] #returns positions of best and second best'''

def tournamentTwo(fitnessList, totalFitScore):
    one = chooseRandomIndividual(fitnessList, totalFitScore)
    two = chooseRandomIndividual(fitnessList, totalFitScore)
    return one if fitnessList[one] > fitnessList[two] else two
    

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
        #multiplied by 5 to increase the weight so that it'll be closer importance to overlapping
        
        if area>rectValues[counter]:
            achievement = (1/(area/rectValues[counter]))
        else:
            achievement = (area/rectValues[counter]) #a percentage of how close it is the what it needs to be
        
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
                
        score = score + achievement**4
        counter = counter + 1

    return score
'''
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
 '''   
def copyX(population, totalFitScore, copyProportion, fitnessList):
    totalCopies = len(population)*copyProportion
    amount = totalCopies
    copied = []
    noInTournament = 4
    retries = 0

    while amount >= 0:
        #print(amount)
        '''
        randIndPositions = tournament(noInTournament, fitnessList, totalFitScore)
        if randIndPositions[0] not in copied:
            randIndPosition = randIndPositions[0]
        elif randIndPositions[1] not in copied:
            randIndPosition = randIndPositions[1]
        else:
            randIndPosition = randIndPositions[2]
        '''
        #randIndPosition = chooseRandomIndividual(fitnessList, totalFitScore)
        randIndPosition = tournamentTwo(fitnessList, totalFitScore)
        '''
        while population[randIndPosition] in copied: #makes sure the same person isn't copied more than once
            #print('retry')
            #retries = retries +1
            #print(retries)
            randIndPositions = tournament(noInTournament, fitnessList, totalFitScore)
            if randIndPositions[0] not in copied:
                randIndPosition = randIndPositions[0]
            elif randIndPositions[1] not in copied:
                randIndPosition = randIndPositions[1]
            else:
                randIndPosition = randIndPositions[2]
            #print('retry at '+str(randIndPosition))
        '''
        
        #print(str(fitnessList[randIndPosition])+' at '+str(randIndPosition))
        
        copied.append(population[randIndPosition])

        amount = amount - 1
        
    #rectValues = [0.5, 0.2, 0.1, 1.5, 0.5]
    #print(fitness(copied, rectValues)[1])
    return copied

def crossover(population, totalFitScore, crossoverProportion, fitnessList):
    totalOffspring = len(population)*crossoverProportion
    #5 rectangles
    #4 features of each rectangle
    numOfRec = 5
    
    offSpring = []
    while totalOffspring > 0:
        #randIndPosition = chooseRandomIndividual(fitnessList, totalFitScore)
        #individualOne = population[randIndPosition]
        #randIndPositionTwo = chooseRandomIndividual(fitnessList, totalFitScore)
        '''
        while randIndPositionTwo == randIndPosition: #making sure two different parents are chosen
            randIndPositionTwo = chooseRandomIndividual(fitnessList, totalFitScore)
        '''
        #individualTwo = population[randIndPositionTwo]
        '''
        noInTournament = 2
        parents = tournament(noInTournament, fitnessList, totalFitScore)
        individualOne = population[parents[0]]
        individualTwo = population[parents[1]]
        '''
        individualOne = population[tournamentTwo(fitnessList, totalFitScore)]
        individualTwo = population[tournamentTwo(fitnessList, totalFitScore)]

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
        print("Average: "+str(sum(fitnessList[1])/len(fitnessList[1])))
        print("Median: "+str(statistics.median(fitnessList[1])))
        findBest(population, fitnessList[1])
        #invertScores = invertFitList(fitnessList) #gives the best score the biggest score
        #ePL = elongatedPopList(population, fitnessList) #makes copies of each individual in accordance with its fitness score
        #print('')
        copy = copyX(population, fitnessList[0], 1-crossoverProportion, fitnessList[1])
        offspring = crossover(population, fitnessList[0], crossoverProportion, fitnessList[1])
        population = copy + offspring
        population = mutate(population, mutationRate)
        fitnessList = fitness(population, rectValues)

        #print(population)
        
        generations = generations - 1
        print('')

    return findBest(population, fitnessList[1])
    

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
    '''
    for score in fitnessList:
        print(score)
    
    print()
    '''
    return population[bestPosition]

rectValues = [0.5, 0.2, 0.1, 1.5, 0.5]
geneticInfo = geneticAlgorithm(5000, 0, 0, rectValues)

##################################################################
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

rects=[]

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
patch1 = patches.PathPatch(path1, facecolor=(1,0,0,0.5), lw=2)
patch2 = patches.PathPatch(path2, facecolor=(0,1,0,0.5), lw=2)
patch3 = patches.PathPatch(path3, facecolor=(0,0,1,0.5), lw=2)
patch4 = patches.PathPatch(path4, facecolor=(0.5,0.5,0,0.5), lw=2)
patch5 = patches.PathPatch(path5, facecolor=(0.5,0,0.5,0.5), lw=2)
ax.add_patch(patch1)
ax.add_patch(patch2)
ax.add_patch(patch3)
ax.add_patch(patch4)
ax.add_patch(patch5)
ax.set_xlim(-0.2,1.2)
ax.set_ylim(-0.2,1.2)
plt.show()
