import numpy as np
import pandas as pd
import random as rd
import copy
import time
from random import randint
import matplotlib.pyplot as plt
from itertools import combinations_with_replacement

#Item
NUMBER_OF_ITEMS = 7
ITEM_MAX_VALUE = 20
ITEM_MAX_WEIGHT = 20
#Knapsack
KNAPSACK_MAX_WEIGHT = 60
BEST_COMBINATION_VALUE = 36
#Algorithm
NUMBER_OF_GENERATIONS = 100
POPULATION = 100
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.5

def main():
    #Postavljanje predmeta
    
    items = []
    for i in range(NUMBER_OF_ITEMS):
        items.append(Item(rd.randint(1, ITEM_MAX_WEIGHT), rd.randint(1, ITEM_MAX_VALUE)))
    """
    items = [Item(12, 4), Item(2, 2), Item(1, 2), Item(1, 1), Item(4, 10)]
    """
    print("************************\n-==|    Items      |==-\n------------------------\nIndex    Weight  Value")
    for item in items:
        print(items.index(item), "\t", item.weight, "\t", item.value)
    print("************************")

    #Postavljanje početne populacije ruksaka
    starting_population = []
    for i in range(POPULATION):
        starting_population.append(Knapsack())

    #Konvencionalni algoritam
    startKonvencional = time.time()
    maxValue = konvencionalnialgoritam(items)
    endKonvencional = time.time()
    timeKonvencional = endKonvencional-startKonvencional
    
    #Glavna funkcija
    algorithm(items, starting_population, maxValue)

    
    print("Konvencionalan algoritam - max value = ", maxValue, ", time: ", timeKonvencional)






def mutation2(population):
    for knapsack in population:
        if rd.random()<MUTATION_RATE:
            knapsack.items[rd.randint(0, NUMBER_OF_ITEMS-1)] = rd.randint(0, 3)
    return population 

def crossover2(parents):
    children = []
    #Presjek kromosoma
    crossPoint = rd.randint(1, NUMBER_OF_ITEMS-1)

    #Križanje roditelja, stvaranje djece
    for i in range(0, len(parents), 2):
        temp1 = copy.deepcopy(parents[i].items)
        temp2 = copy.deepcopy(parents[i+1].items)
    
        for j in range(crossPoint, NUMBER_OF_ITEMS):
            temp1[j], temp2[j] = temp2[j], temp1[j]

        #Vrati djecu samo ako je pogođena šansa za križanje
        if rd.random()<CROSSOVER_RATE:
            children.append(Knapsack(temp1))
        else:
            children.append(Knapsack(copy.deepcopy(parents[i].items)))
        if rd.random()<CROSSOVER_RATE:
            children.append(Knapsack(temp2))
        else:
            children.append(Knapsack(copy.deepcopy(parents[i+1].items)))
        if i+2>=len(parents)-1:
            break

    if len(children)+len(parents)!=POPULATION:
        children.append(Knapsack(copy.deepcopy(parents[rd.randint(0, len(parents)-1)].items)))
    return children

def  selection2(population):
    #Populacija se sortira po rezultatima fitnes funkcije (fitnessScore)
    parents = population
    parents.sort(key=lambda x: x.fitnessScore, reverse=True)
    #Polovica populacije se uzima za roditelje sa kojima će se raditi crossover
    parents = parents[0:int(POPULATION/2)]
    return parents

def fitness(items, population):
    #For petlja koja prolazi svaki ruksak u populaciji i 
    # određuje ukupnu vrijednost i težinu stvari
    for knapsack in population:
        items_weight = 0
        items_value = 0
        for i in range(NUMBER_OF_ITEMS):
            items_weight += knapsack.items[i]*items[i].weight
        for i in range(NUMBER_OF_ITEMS):
            items_value += knapsack.items[i]*items[i].value

        #Ako je ukupna težina stvari > max težine ruksaka, postavi fitness vrijednost na 0
        if items_weight>KNAPSACK_MAX_WEIGHT:
            knapsack.fitnessScore = 0
        else:
            knapsack.fitnessScore = items_value

def printPopulation(population, generationNumber, items, maxValue):
    print("Generation ", generationNumber)
    fitnesses = [0] * POPULATION
    maxFitnessOfPopulation = 0
    counter = 0
    for a in population:
        items_weight = 0
        items_value = 0
        for i in range(NUMBER_OF_ITEMS):
            items_weight += a.items[i]*items[i].weight
        for i in range(NUMBER_OF_ITEMS):
            items_value += a.items[i]*items[i].value
        if a.fitnessScore != None:
            fitnesses[counter]=a.fitnessScore
            if a.fitnessScore > maxFitnessOfPopulation:
                maxFitnessOfPopulation = a.fitnessScore
        print(a, "weight: ", items_weight, ", value:", items_value)
        counter += 1
    print("Average fitness score in population: ", sum(fitnesses)/len(fitnesses))
    print("Best fitness score in population: ", maxFitnessOfPopulation)
    print("How close to best solution: ", maxFitnessOfPopulation/maxValue)
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")    

def algorithm(items, population, maxValue):
    bestSolutionDiscovered = False

    startGeneticAlgorithm = time.time()
    for i in range(NUMBER_OF_GENERATIONS):
        if bestSolutionDiscovered==True:
            break

        fitness(items, population)
        parents = selection2(population)
        children = crossover2(parents)
        population = parents + children
        population = mutation2(population)

        #Provjera je li najbolja jedina već izučena
        for knapsack in population:
            if knapsack.fitnessScore == maxValue:
                
                printPopulation(population, i, items, maxValue)
                print("Pronađeno najbolje rješenje u ", i, "-toj generaciji.")
                bestSolutionDiscovered = True
                break
                
        if i==0:
            printPopulation(population, i, items, maxValue)
        if i==NUMBER_OF_GENERATIONS-1:
            printPopulation(population, i, items, maxValue)
    
    
    endGeneticAlgorithm = time.time()
    geneticAlgorithmTime = endGeneticAlgorithm - startGeneticAlgorithm
    print("Vrijeme genetičkog algoritma: ", geneticAlgorithmTime)    


def konvencionalnialgoritam(items):
    bestCombinatioValue = 0
    bestCombinationToSave = [0] * NUMBER_OF_ITEMS
    bestCombination = [0] * NUMBER_OF_ITEMS

    
    a = True
    while(a):
        for j in range(4):
            if a==False:
                    break
            if bestCombination[0]==3:
                for k in range(NUMBER_OF_ITEMS):
                    if bestCombination[k]==3:
                        bestCombination[k]=0
                        if k+1==NUMBER_OF_ITEMS:
                            a=False
                            break
                        if bestCombination[k+1]!=3:
                            bestCombination[k+1]+=1
                            break

                        
                        
            else:
                bestCombination[0] += 1
            items_weight = 0
            items_value = 0
            for i in range(NUMBER_OF_ITEMS):
                items_weight += bestCombination[i]*items[i].weight
            for i in range(NUMBER_OF_ITEMS):
                items_value += bestCombination[i]*items[i].value
            if items_weight <= KNAPSACK_MAX_WEIGHT:
                if items_value>bestCombinatioValue:
                    bestCombinatioValue=items_value
                    bestCombinationToSave = copy.deepcopy(bestCombination)
    print(bestCombinationToSave)
    return bestCombinatioValue


class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

    def __str__(self):
        return f"Weight: {self.weight}\tValue: {self.value}"

class Knapsack:
    def __init__(self, items=None):
        self.fitnessScore = None

        if(items==None):
            self.items = [0] * NUMBER_OF_ITEMS
            for i in range(NUMBER_OF_ITEMS):
                self.items[i] = rd.randint(0, 3)
        else:
            self.items = items

    def __str__(self):
        return ' '.join(str(i) for i in self.items)

if __name__=="__main__":
   main()

