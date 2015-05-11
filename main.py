__author__ = 'Den'

from random import random, randint
from numpy import sum

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
    for i in range(len(x)):
        if f[i] == 0:
            f1[x[i]] += 1
        else:
            f2[x[i]] += 1
    sum_f1 = sum(f1)
    sum_f2 = sum(f2)
    f1 = [i / sum_f1 for i in f1]
    f2 = [i / sum_f2 for i in f2]
    return f1, f2

def getFirstDeckProbability(f):
    return 1 - sum(f)/len(f)


def getValuesProbabilities(f1, f2, pf1):
    return [f1[i] * pf1 + f2[i] * (1 - pf1) for i in range(n)]

def getDepedentDeckProbabilities(f1, f2, pf1, px):
    return [f1[i] * pf1 / px[i] for i in range(n)], [f2[i] * (1 - pf1) / px[i] for i in range(n)]

def analizeExperiment(x, f):
    f1, f2 = getDistributions(x, f)
    pf1 = getFirstDeckProbability(f)
    pf1x, pf2x = getDepedentDeckProbabilities(f1, f2, pf1, getValuesProbabilities(f1, f2, pf1))

    #count error:
    err1 , err2 = 0, 0
    for i in range(n):
        err1 += (pf1x[i] - sum([1 for j in range(len(f)) if f[j] == 0 and x[j] == i]) / sum([1 for j in range(len(f)) if x[j] == i])) ** 2
        err2 += (pf2x[i] - sum([1 for j in range(len(f)) if f[j] == 1 and x[j] == i]) / sum([1 for j in range(len(f)) if x[j] == i])) ** 2
    return err1 + err2

def evolutionaryMinimizer(f, length):
    iterations_without_changes = 0
    x = [randint(0, 1) for i in range(length)]
    current_value = f(x)
    while iterations_without_changes < 1000:
        i = randint(0, length - 1)
        x[i] = 1 - x[i]
        new_value = f(x)
        if new_value <= current_value:
            current_value = new_value
            iterations_without_changes = 0
        else:
            x[i] = 1 - x[i]
            iterations_without_changes += 1
    return x

f1, f2 = generateDistribution(), generateDistribution()
x, f = generateExperiment(f1, f2, l, switch)
print(x)
print(f)

##here we should find a solution minimizig the result of analizeExperiment on vector f  with given vector x
def vectorResult(vector):
    return analizeExperiment(x, vector)

result = evolutionaryMinimizer(vectorResult, l)
print("result:", analizeExperiment(x, result), "real distribution:", analizeExperiment(x, f))
print(result)
print(f)
# f = [randint(0, 1) for i in range(l)]
# print(analizeExperiment(x, f))