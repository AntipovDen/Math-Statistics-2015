__author__ = 'Den'

from random import random, randint
from numpy import sum
from math import sqrt, log

n = 10
l = 100
switch = 1/3

def generateDistribution():
    x = [random()]
    for i in range(n - 1):
        x.append(x[-1] + random())
    return [i / x[-1] for i in x]

def generateExperiment(f1, f2, length, switchProbability):
    f = []
    currentDeck = 0
    for i in range(length):         #generate distribution of decks in time
        if random() < switchProbability:
            currentDeck = 1 - currentDeck
        f.append(currentDeck)

    x = []
    for i in range(length):         #generate random values by the deck distribution
        r = random()
        if f[i] == 1:
            x.append(min([k for k in range(len(f2)) if f2[k] > r]))
        else:
            x.append(min([k for k in range(len(f1)) if f1[k] > r]))
    return x, f

def getDistributions(x, f):
    #assume that we know all possible random values. they are from 0 to n (not inclusive)

    f1 = [0] * n
    f2 = [0] * n
    for i in range(l):
            if f[i] == 0:
                f1[x[i]] += 1
            else:
                f2[x[i]] += 1
    for i in range(n):
        if f1[i] == 0:
            f1[i] += 0.5
        if f2[i] == 0:
            f2[i] += 0.5
    sum_f1 = sum(f1)
    sum_f2 = sum(f2)
    f1 = [i / sum_f1 for i in f1]
    f2 = [i / sum_f2 for i in f2]
    return f1, f2

#functions for my method
def getFirstDeckProbability(f):
    return 1 - sum(f)/len(f)

def getValuesProbabilities(f1, f2, pf1):
    return [f1[i] * pf1 + f2[i] * (1 - pf1) for i in range(n)]

def getDepedentDeckProbabilities(f1, f2, pf1, px):
    return [f1[i] * pf1 / px[i] for i in range(n)], [f2[i] * (1 - pf1) / px[i] for i in range(n)]

def analizeExperimentMyMethod(x, f):
    f1, f2 = getDistributions(x, f)
    pf1 = getFirstDeckProbability(f)
    pf1x, pf2x = getDepedentDeckProbabilities(f1, f2, pf1, getValuesProbabilities(f1, f2, pf1))

    #count error:
    err1 , err2 = 0, 0
    for i in range(n):
        err1 += (pf1x[i] - sum([1 for j in range(len(f)) if f[j] == 0 and x[j] == i]) / sum([1 for j in range(len(f)) if x[j] == i])) ** 2
        err2 += (pf2x[i] - sum([1 for j in range(len(f)) if f[j] == 1 and x[j] == i]) / sum([1 for j in range(len(f)) if x[j] == i])) ** 2
    return err1 + err2


#functions for some indian method
def bhattacharyyaDistance(distributions):
    f1, f2 = distributions
    s = sum([sqrt(f1[i] * f2[i]) for i in range(n)])
    if s == 0:
        return -float('infinity')
    return log(s)

##Evolution
populationSize = 100
newGenSize = 80

def generateIndividual():
    x =[]
    cur = 1
    for i in range(l):
        if random() < switch:
            cur = 1 - cur
        x.append(cur)
    return x

def selectParents(population, f):
    values = [f(p) for p in population]
    for i in range(1, populationSize):
        values[i] += values[i - 1]
    values = [i/ values[-1] for i in values]
    r = random()
    par1 = population[min([k for k in range(populationSize) if values[k] > r])]
    r = random()
    par2 = population[min([k for k in range(populationSize) if values[k] > r])]
    return par1, par2

def crossingover(parents):
    par1, par2 = parents
    i = randint(0, l - 1)
    return par1[:i] + par2[i:], par2[:i] + par1[i:]

def evolutionaryMinimizer(f, length):
    population = [generateIndividual() for i in range(populationSize)]
    for i in range(1000):
        if i % 10 == 0:
            print(i)
        new_generation = []
        for i in range(newGenSize // 2):
            c1, c2 = crossingover(selectParents(population, f))
            new_generation += [c1, c2]
        tmp = [(f(population[i]), population[i]) for i in range(populationSize)]
        tmp.sort()
        population = [t[1] for t in tmp[:(populationSize - newGenSize)]] + new_generation
    return min([(f(population[i]), population[i]) for i in range(populationSize)])

def mutationMinimizer(f, length):
    iterations_without_changes = 0
    x = [randint(0, 1) for i in range(length)]
    current_value = f(x)
    while iterations_without_changes < 1000:
        x1 = []
        cur_source = 1
        for i in range(length):
            if random() < switch:
                cur_source = 1 - cur_source
            x1.append(cur_source)
        # i = randint(0, length - 1)
        # x[i] = 1 - x[i]

        new_value = f(x)
        if new_value <= current_value:
            current_value = new_value
            x = x1
            iterations_without_changes = 0
        else:
            # x[i] = 1 - x[i]
            iterations_without_changes += 1
    return x

f1, f2 = generateDistribution(), generateDistribution()
x, f = generateExperiment(f1, f2, l, switch)
print(x)
print(f)

##here we should find a solution minimizig the result of analizeExperimentMyMethod on vector f  with given vector x
def vectorResult(vector):
    return analizeExperimentMyMethod(x, vector)

def vectorResultBhattacharyya(vector):
    return bhattacharyyaDistance(getDistributions(x, vector))


result = evolutionaryMinimizer(vectorResultBhattacharyya, l)[1]
print(result)
print(f)

print("result:", bhattacharyyaDistance(getDistributions(x, result)),
      "real distribution:", bhattacharyyaDistance(getDistributions(x, f)))
# f = [randint(0, 1) for i in range(l)]
# print(analizeExperimentMyMethod(x, f))