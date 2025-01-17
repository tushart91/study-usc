#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################
# @file     agent.py
# @author   Tushar Tiwari
# @email    ttiwari@usc.edu
# @course   Probabilistic Reasoning/HW6
# @prof     Prof. Ram Nevatia
# @date     2015-04-03
########################################

import random
import math

def agent():

    # Initialize probability values
    B = [0.998, 0.002]
    E = [0.999, 0.001]

    # a0      e0     e1
    ABE = [[[0.998, 0.4], #b0
            [0.15, 0.07]],#b1
    # a1    e0     e1
         [[0.002, 0.6],   #b0
          [0.85, 0.93]]]  #b1
    # j1     a0    a1
    jTA = [[0.02, 0.88],  #t0
           [0.03, 0.45]]  #t1

    # m0     a0    a1
    mNA = [[0.99, 0.25],  #n0
           [0.999, 0.75]] #n1

    T = [0.2, 0.8]
    N = [0.75, 0.25]

    evidence = {
        "E": 0, "B": 0, "T": 0, "N": 0, "A": 0
    }
    old_value = {
        "E": [0], "B": [0], "T": [0], "N": [0], "A": [0]
    }
    value = {
        "E": [0], "B": [0], "T": [0], "N": [0], "A": [0]
    }
    time = 1

    # initial random assignment B = 0, A = 0, T = 0, N = 0
    print "Minimum separation for stable distribution: 0.00000000000001 and 1000000T"

    print "Initial Assignment"
    for i in evidence.keys():
        print i + ":", evidence[i]
    print

    def computeT():
        # compute T
        # ø(j,T,A).ø(T)
        jTa = reduce_column(jTA, evidence["A"])
        jTa = pointwise_multiply(jTa, T)
        value["T"] = normalize(jTa)
        evidence["T"] = random_assignment(value["T"])

    def computeN():
        # compute N
        # ø(m,N,A).ø(N)
        mNa = reduce_column(mNA, evidence["A"])
        mNa = pointwise_multiply(mNa, N)
        value["N"] = normalize(mNa)
        evidence["N"] = random_assignment(value["N"])

    def computeA():
        # compute A
        # ø(A,b,e).ø(j,t,A).ø(m,n,A)
        AbE = [reduce_row(ABE[0], evidence["B"]), reduce_row(ABE[1], evidence["B"])]
        Abe = reduce_column(AbE, evidence["E"])

        jtA = reduce_row(jTA, evidence["T"])
        mnA = reduce_row(mNA, evidence["N"])

        Abe = pointwise_multiply(pointwise_multiply(jtA, mnA), Abe)
        value["A"] = normalize(Abe)
        evidence["A"] = random_assignment(value["A"])

    def computeB():
        # compute B
        # ø(B).ø(a|B,e)
        aBE = reduce_matrix(ABE, evidence["A"])

        aBe = reduce_column(aBE, evidence["E"])
        aBe = multiply(pointwise_multiply(aBe, B), E[evidence["E"]])
        value["B"] = normalize(aBe)
        evidence["B"] = random_assignment(value["B"])

    def computeE():
        # compute P(E)
        # ø(E).ø(a|b,E)
        aBE = reduce_matrix(ABE, evidence["A"])

        abE = reduce_row(aBE, evidence["B"])
        abE = multiply(pointwise_multiply(abE, E), B[evidence["B"]])
        value["E"] = normalize(abE)
        evidence["E"] = random_assignment(value["E"])

    options = {
        0: computeT,
        1: computeN,
        2: computeA,
        3: computeB,
        4: computeE
    }

    while(True):

        num = random.randint(0, 4)

        options[num]()

        flag = False
        if time !=0 and time % 1000000 == 0:
            flag = True
            for i in value.keys():
                if math.fabs(value[i][0] - old_value[i][0]) > 0.00000000000001:
                    flag = False
                    break
            for i in evidence.keys():
                old_value[i] = value[i]

        if flag: break
        if time % 100000 == 0:
            print "T:", time
            for i in evidence.keys():
                print i + ":", evidence[i], "\t", value[i]
            print

        time += 1
    print
    print "Convergence at T =", time  
    print "Assignment:", evidence
    for i in evidence.keys():
        print i + ":", value[i]

def multiply(oneD, num):
    ret = []
    for i in range(len(oneD)):
        ret.append(oneD[i]*num)
    return ret

def reduce_column(twoD, sel):
    ret = []
    for i in range(len(twoD)):
        ret.append(twoD[i][sel])
    return ret

def reduce_row(twoD, sel):
    ret = []
    for i in range(len(twoD[sel])):
        ret.append(twoD[sel][i])
    return ret

def reduce_matrix(threeD, sel):
    ret = []
    for i in range(len(threeD[sel])):
        ret.append([])
        for j in range(len(threeD[sel][i])):
            ret[i].append(threeD[sel][i][j])
    return ret

def pointwise_multiply(oneD1, oneD2):
    ret = []
    for i in range(len(oneD1)):
            ret.append(oneD1[i] * oneD2[i])
    return ret

def random_assignment(oneD):
    rand = random.uniform(0.0, 1.0)
    if rand <= oneD[0]:
        return 0
    return 1

def normalize(oneD):
    total = sum(oneD)
    ret = []
    for i in oneD:
        ret.append(i/total)
    return ret

if __name__ == "__main__":
    agent()
