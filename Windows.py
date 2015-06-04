__author__ = 'dantipov'

from random import random, randint
from numpy import sum
from math import exp, sqrt, log
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
    # try to calculate probabilities

    #p(x[i] = x)
    p_x = [x.count(i) for i in range(n)]
    #p(f[i] = 0| x[i] = x)
    p_f0_with_x = [5/8, 5/8, 5/8, 5/8, 5/8, 1/4]
    #p_f0_with_x = [1/(1 + 4 ** ((abs(i - min_exp) - abs(i - max_exp)) / (max_exp - min_exp))) for i in range(n)]

    #p(x[i] = x | f[i] = 0/1)
    p_x_with_f0 = [p_f0_with_x[i] * p_x[i] / sum([p_f0_with_x[j] * p_x[j] for j in range(n)]) for i in range(n)]
    p_x_with_f1 = [(1 - p_f0_with_x[i]) * p_x[i] / sum([( 1 - p_f0_with_x[j]) * p_x[j] for j in range(n)]) for i in range(n)]

    #dinamic calculation of p(f[i] = 0 | x[i] = x):
    #p_x_with_switch -- p(x[i] = x | switch)
    #p_x_with_no_switch -- p(x[i] = x | no switch)
    #p_switch_with_x -- p(switch | x[i] = x)
    #p_f0 -- p(f[i] = 0 | x[i] = x)

    p_f0 = [p_f0_with_x[x[0]]]

    for i in range(1, len(x)):
        p_x_with_switch = p_x_with_f0[x[i]] * (1 - p_f0[-1]) + p_x_with_f1[x[i]] * p_f0[-1]
        p_x_with_no_switch = p_x_with_f0[x[i]] * p_f0[-1] + p_x_with_f1[x[i]] * (1 - p_f0[-1])

        p_switch_with_x = p_x_with_switch * switch / (p_x_with_switch * switch + p_x_with_no_switch * (1 - switch))
        p_f0.append(p_f0[-1] * (1 - p_switch_with_x) + (1 - p_f0[-1]) * p_switch_with_x)
    return p_f0

    # try to make result based on expectation vibration

    # result = [0] * (window_size + 1)
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
        res.append(windowExpectation(window2) - windowExpectation(window1))
        # w1d = [0] * n
        # w2d = [0] * n
        # for j in window1:
        #     w1d[j] += 1
        # for j in window2:
        #     w2d[j] += 1
        # w1d = [j/sum(w1d) for j in w1d]
        # w2d = [j/sum(w2d) for j in w2d]
        # next_res = sum([sqrt(w1d[j] * w2d[j]) for j in range(n)])
        # if next_res == 0:
        #     res.append(float('inf'))
        # else:
        #     res.append(-log(next_res))
    res = [0] + res
    for i in range(50):
        res = smooth(res)
    return res

f1, f2 = [1/6, 1/3, 1/2, 2/3, 5/6, 1], [1/10, 1/5, 3/10, 2/5, 1/2, 1]
x, f = generateExperiment(f1, f2, l, switch)

print(x)
print(f)
print("expectations:", expectation(f1), expectation(f2))

res = windowAnalysing(x, int(1/switch))

print(f)
print(res)

x1 = [i for i in range(l) if f[i] == 0]
x2 = [i for i in range(l) if f[i] == 1]

y1 = [res[x] for x in x1]
y2 = [res[x] for x in x2]

plt.plot(x1, y1, 'bo', label='honest dice')
plt.plot(x2, y2, 'ro', label='dishonest dice')
plt.legend(loc=1)
plt.xlabel("i")
plt.ylabel("p(S[i] = 0)")
plt.show()