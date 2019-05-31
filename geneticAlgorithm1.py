from random import *
import math
import statistics

#def dist(x, y, a, b):return math.sqrt( (x-a)**2 + (y-b)**2 )

def randRect(): #creates random rectangle
    width = (randint(1, 100))/100
    height = (randint(1, 100))/100
    x = (randint(1, 100))/100
    y = (randint(1, 100))/100
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

def fitnessScore(individual, rectValues):
    score = 0
    counter = 0
    for rect in individual:
        
        width = rect[0]
        height = rect[1]
        area = width*height

        x = rect[2]
        y = rect[3]

        #check to see if the area of the rectangle is the correct size
        if area>rectValues[counter]:
            punishment =((area - rectValues[counter])*10)
        else:
            punishment =((rectValues[counter] - area)*10)

        score = score + punishment

        #check to see if the rectangle's area is inside perimeter
        if width/2 + x > 1:
            score = score + ((width/2 + x) - 1)*10 # how much its out of the perimeter on the right side

        if width/2 - x < 0:
            score = score + (x - width/2)*10 # how much its out of the perimeter on the left side

        if height/2 + y > 1:
            score = score + ((height/2 + y) - 1)*10 # how much its out of the perimeter on the bottom

        if height/2 - x < 0:
            score = score + (x - height/2)*10 #how much its out of the perimeter on the top

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

                #topleft overlap
                if botRightTwo[0]>topLeftOne[0] and botRightTwo[1]>topLeftOne[1]:
                    widthOfOL = botRightTwo[0] - topLeftOne[0]
                    heightOfOL = botRightTwo[1] - topLeftOne[1]
                    areaOfOL = widthOfOL*heightOfOL
                    score = score + areaOfOL*10

                #topright overlap
                if botLeftTwo[0]<topRightOne[0] and botLeftTwo[1]>topRightOne[1]:
                    widthOfOL =  topRightOne[0] - botLeftTwo[0]
                    heightOfOL = botLeftTwo[1] - topRightOne[1]
                    areaOfOL = widthOfOL*heightOfOL
                    score = score + areaOfOL*10
                    
                #botleft overlap
                if topRightTwo[0]>botLeftOne[0] and topRightTwo[1]<botLeftOne[1]:
                    widthOfOL = topRightTwo[0] - botLeftOne[0]
                    heightOfOL = botLeftOne[1] - topRightTwo[1]
                    areaOfOL = widthOfOL*heightOfOL
                    score = score + areaOfOL*10

                #botright overlap
                if topLeftTwo[0]<botRightOne[0] and topLeftTwo[1]<botRightOne[1]:
                    widthOfOL = botRightOne[0] - topLeftTwo[0]
                    heightOfOL = botRightOne[1] - topLeftTwo[1]
                    areaOfOL = widthOfOL*heightOfOL
                    score = score + areaOfOL*10
      
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
    #print("amount: "+str(amount))
    while amount > 0:
        choice = randint(1, len(ePL))-1
        while ePL[choice] in copied: #makes sure the same person isn't copied more than once
            choice = randint(1, len(ePL))-1
            
        copied.append(ePL[choice])
        #print("amount: "+str(amount))
        amount = amount - 1
    print("finished copy")
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

def mutate(population, mutationRate): #randomly selects a few rectangles and replaces them with a new random rectangle
    rectangles = 5
    features = 4
    totalMutation = len(population)*mutationRate
    counter = 0
    while counter < totalMutation:
        randRect = randint(1, rectangles)-1
        randFeature = randint(1, features)-1
        individual = randint(1, len(population))-1
        population[individual][randRect][randFeature] = (randint(1, 100))/100
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
        invertScores = invertFitList(fitnessList) #gives the best score the biggest score
        ePL = elongatedPopList(population, invertScores) #makes copies of each individual in accordance with its fitness score
        print("beginning copy")
        copy = copyX(population, ePL, 1-crossoverProportion, fitnessList)
        print("copied")
        offspring = crossover(population, ePL, crossoverProportion, fitnessList)
        print("crossovered")
        population = copy + offspring
        population = mutate(population, mutationRate)
        print("mutated")
        fitnessList = fitness(population, rectValues)
        
        generations = generations - 1

    return findBest(population, fitnessList)
    

def findBest(population, fitnessList):
    bestPosition = 0
    bestScore = 1000
    counter = 0
    worstScore = 0
    
    for score in fitnessList:
        if score>worstScore:
            worstScore = score
        if score<bestScore:
            bestScore = score
            bestPosition = counter
        counter = counter + 1
    print('bestScore: '+str(bestScore))
    print('worstScore: '+str(worstScore))
    print(population[bestPosition])
    print()

    return population[bestPosition]

rectValues = [0.5, 0.2, 0.1, 1.5, 0.5]
geneticInfo = geneticAlgorithm(5000, 0.3, 0.01, rectValues)

    
