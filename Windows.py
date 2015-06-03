__author__ = 'dantipov'

from random import random, randint
from numpy import sum
from math import exp
from matplotlib import pyplot as plt


n = 6
l = 100
switch = 1/10

def generateDistribution():
    x = [random()]
    for i in range(n - 1):
        x.append(x[-1] + random())
    return [i / x[-1] for i in x]

def expectation(distribution):
    return sum([(distribution[i + 1] - distribution[i]) ** 2 for i in range(n - 1)]) + distribution[0] ** 2

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

def windowExpectation(window):
    return sum(window)/len(window)
    # dist = [0] * n
    # for i in window:
    #     dist[i] += 1
    # s = sum(dist)
    # return sum([(d / s) ** 2 for d in dist])

def smooth(function):
    res = [f for f in function]
    for i in range(1, len(function) - 1):
        function[i] = function[i] / 2 + (function[ i + 1] + function[i - 1]) / 4
    return function


def windowAnalysing(x, window_size):
    window_expectations = []
    for i in range(len(x) - window_size):
        window_expectations.append(windowExpectation(x[i:i + window_size]))

    min_exp, max_exp = min(window_expectations), max(window_expectations)
    print("min expectation:", min_exp)
    print("max expectation:", max_exp)

    plt.plot([i + window_size for i in range(len(window_expectations))], window_expectations, 'r-')
    # try to calculate probabilities
    for i in range(10):
        window_expectations = smooth(window_expectations)

    # def distance_prob(a):
    #     return 1 / (1 + 1.5 ** (abs(a - min_exp) - abs(a - max_exp)))
    #     # if a == 5:
    #     #     return 0.25
    #     # return 0.625
    #
    # print([distance_prob(a) for a in range(6)])
    # p = [distance_prob(x[0])] #probability that x_i was given by the source with min expectation
    #
    # for i in range(1, len(x)):
    #     p_no_switch, p_switch  = (1 - switch) * distance_prob(x[i]), switch * (1 - distance_prob(x[i]))
    #     if p[-1] > 0.5:
    #         p.append(p_no_switch)
    #     else:
    #         p.append(p_switch)

    # try to make result based on expectation vibration

    # result = [0] * (window_size + 1) #TODO: analyse the begining of the vetor
    # for i in range(len(window_expectations) - 1):
    #     if window_expectations[i] > window_expectations[i + 1]:
    #         result.append(0)
    #     elif window_expectations[i] < window_expectations[i + 1]:
    #         result.append(1)
    #     else:
    #         result.append(result[-1])

    # smart try with expctation vibration
    result = [0] * (window_size + 1)
    for i in range(1, len(window_expectations) - 1):
        if (window_expectations[i] - window_expectations[i - 1] < window_expectations[i + 1] - window_expectations[i]):
            result.append(0)
        else:
            result.append(1)
    result.append(0)

    # return [0] * window_size + window_expectations
    return result

def twoWindowsAnalysing(x):
    window_size = int(1/switch)
    res = []
    for i in range(1, len(x)):
        window1 = x[max(i - window_size, 0):i]
        window2 = x[i:min(i + window_size, len(x))]
        res.append(sum(window1)/len(window1) - sum(window2)/len(window2))
    res = [0] + res
    for i in range(50):
        res = smooth(res)
    return res

f1, f2 = [1/6, 1/3, 1/2, 2/3, 5/6, 1], [1/10, 1/5, 3/10, 2/5, 1/2, 1]
x, f = generateExperiment(f1, f2, l, switch)

print(x)
print(f)
print("expectations:", expectation(f1), expectation(f2))

res = twoWindowsAnalysing(x)

print(f)
print(res)


#exit(0)
x1 = [i for i in range(l) if f[i] == 0]
x2 = [i for i in range(l) if f[i] == 1]

print(x1)
print(x2)

y1 = [res[x] for x in x1]
y2 = [res[x] for x in x2]

plt.plot(x1, y1, 'bo', x2, y2, 'ro')
plt.show()