#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from numpy import * #es para random
import math
import sys
import random
#graficar con gnuplot

Gmax = 1000
t = 0    #current generation
n = 2        # number of variables
E = 0.00000001 #Error (Epsilon), Python's precision: 0.000000000000001
s = 10    #standard deviation
C = 0.817    #constant of Ingo Rechenberg & Hans-Paul Schwefel
Mu = Lambda = 200
minValue = -65.536
maxValue = 65.536
Sigma = [maxValue / 2]

class guy:
    def __init__(self):
        self.g = []
        self.d = []
        self.f = 0

def seed(n):
    return [(random.random() * 2 - 1) * maxValue for i in range(n)]

#[random.random() * 65.536 * pow(-1, (i % 2)) for i in range(n)]

def fitness(x):
    #f(xi) = f(x1, x2) = 1.0 / ( 1.0/500 + 1.0 / fj(x1, x2) )
    #fj(x1, x2) = [[(j + 1) + pow(x.g[i] - a[i][j], 6) for i in range(2)] for j in range(25)]

    b = [-32, -16, 0, 16, 32]
    a = [[ b[i % 5] for i in range(25)],[ b[int(i / 5)] for i in range(25)]]

    fj1 = 0.0
    for j in range(25):
        fj = 0.0
        for i in range(2):
            fj += (j + 1) + pow(x.g[i] - a[i][j], 6) # min = 1 max = 8.60973225357416808118889742336 × 10^11 + 25
            # 1/fj max = 1 min = 0.0000000000011614
        fj1 += 1.0 / fj # sum max = 34052522467/8923714800 min
    return 1.0 / (1.0/500.0 + fj1) #24. [2] [-32, -32], 1.99203126216


def mutate(x, t):
    y = guy()
    for i in range(n):
        gi = x.g[i] + Sigma[t] * (random.random() * 2 - 1)

        if gi < minValue:
            gi = minValue
        elif gi > maxValue:
            gi = maxValue

        y.g.append(gi)

    return y

def match( x, x1, success, t):
    if fabs(x.f - x1.f)<E:
        print ("like father like son \n") #"\n Sigma:", sort(Sigma)
        sys.exit(0)
    if x1.f < x.f:
        success[t % 5] = 1 #relative success
        #print "SUCCESS !! t,t%5:", t, t%5
        #success += 1 #absolute success
        return x1, success
    success[t%5] = 0 #relative success
    return x, success

def sigma(Sigma, t, PS):
    if PS >= 1.0/5.0:
        print ("PS:", PS, "; Sigma increases:", Sigma[t-n])
        return Sigma[t-n] / C
    elif PS < 1.0/5.0:
        print ("PS:", PS, "; Sigma reduces:", Sigma[t-n])
        return Sigma[t-n] * C
    #print t, "la sigma no cambia", PS
    #return Sigma[t-n]

def printf(x, t):
    print  (x.g, "Fitness:", x.f)

def distance(people):
    for i in range(Mu):
        people[i].d = []
        for j in range(n):
            people[i].d.append( abs(people[0].g[j] - people[i].g[j]))
    return people

def intercourse(x1, x2):
    child1 = guy()
    child2 = guy()
    position = random.randint(n-1, n-1)

    #for i in range(n):
    child1.g = x1.g[0:position] + x2.g[position:n]
    child2.g = x2.g[0:position] + x1.g[position:n]

    return child1, child2

def seleccionRuleta(people):
    suma = 0.0
    for person in people:
        suma += person.f
    Media = suma/Mu

    ValoresEsperados = []
    for person in people:
        Valor = person.f/ Media
        ValoresEsperados.append(Valor)

    T = sum(ValoresEsperados)
    r = random.random() * T

    suma = 0.0
    i = 0
    for ve in ValoresEsperados:
        suma += ve
        if suma >= r:
            return people[i]
        i += 0

def evolve(people, offspring):
    everyOne = people + offspring
    everyOne = sorted(everyOne, key=lambda llave: llave.f, reverse = False)
    people = everyOne[0:Mu]
    return people


def populate(Mu):
    people = []
    #suma = 0
    for i in range(Mu):
        x = guy()
        x.g = seed(n)
        x.f = fitness(x)
        #suma += x.f
        people.append(x)
    people = sorted(people, key=lambda llave: llave.f, reverse = False)
    people = distance(people)
    return people

def main(t, Gmax):
    success = [ 0 for i in range(5)] #relative success
    #success = 0 #absolute success
    PS = 0    #percentage of success

    people = populate(Mu)

    elitism = people[0]

    while t < Gmax:
        #people = sorted(people, key=lambda llave: llave.d)
        offspring = []
        for i in range(int(Lambda / 2)):
            x1, x2 = intercourse(seleccionRuleta(people), seleccionRuleta(people))
            x1 = mutate(x1, t)
            x2 = mutate(x2, t)
            x1.f = fitness(x1)
            x2.f = fitness(x2)
            offspring.append(x1)
            offspring.append(x2)

        people = evolve(people, offspring)
        offspring = sorted(offspring, key=lambda llave: llave.f)
        #people = offspring
        #people[Mu-1] = x1

        t += 1
        print ("Generation:", t)
        print ("The best:")
        printf(elitism, t)
        print ("The best population's child:")
        printf(offspring[0], t)
        elitism, success = match(elitism, offspring[0], success, t)
        PS = float(sum(success)) / float(5) #relative success
        #PS = float(success)/float(t) #absolute success
        print ("Percentage of Success, success: ", PS, ",", success)
        #print "\nSigma:", Sigma
        #printf(people[0], t)
        #people[Mu-1] = offspring[0]
        #people = sorted(people, key=lambda llave: llave.f)
        if (t % n) == 0:
            Sigma.append(sigma(Sigma, t, PS))
        else:
            Sigma.append(Sigma[t-1])

        print ("\n\n")
        """
        for i in range(Mu):
            printf(people[i], t)
        """

#if __name__ == "__main__":
main(t, Gmax)
