import pysat
import itertools
import random
import sys
from math import sqrt
from pysat.card import *
from pysat.solvers import Minisat22, Solver
from pysat.formula import CNF
import csv
cnf = CNF()
K = int(input())
nv = 0
def var():
    global nv 
    nv += 1
    return nv

def convert_3D(k, l):
    for i in range(len(l)//k):
        yield l[i*k:(i+1)*k]

a = [var() for v in range(((K**2)**3))]
random.shuffle(a)
a1 = list(convert_3D((K**2), list(convert_3D(K**2, a))))
b = [var() for v in range((K**2)**3,2*((K**2)**3))]
random.shuffle(b)
a2 = list(convert_3D((K**2), list(convert_3D(K**2, b))))
c = a + b
V = a1+a2
# each number can appear only one time in a row
for i in range(2*(K**2)):
    for v in range(K**2):
        col = [V[i][j][v] for j in range(K**2)]
        card = pysat.card.CardEnc.equals(lits=col, top_id=nv, bound=1, encoding=0)
        cnf.extend(card.clauses)
        nv = card.nv

# each number can appear only one time in a column
for j in range(K**2):
    for v in range(K**2):
        row = [V[i][j][v] for i in range(K**2)]
        card = pysat.card.CardEnc.equals(lits=row, top_id=nv, bound=1, encoding=0)
        cnf.extend(card.clauses)
        row = [V[i][j][v] for i in range(K**2,2*(K**2))]
        card = pysat.card.CardEnc.equals(lits=row, top_id=nv, bound=1, encoding=0)
        cnf.extend(card.clauses)
        nv = card.nv

# each number can appear only one time in a block
for bi in range(2*K):
    for bj in range(K):
        for v in range(K**2):
            blk = [V[i][j][v] for i in range(bi*K,bi*K+K) for j in range(bj*K,bj*K+K)]
            card = CardEnc.equals(lits=blk, top_id=nv, bound=1, encoding=0)
            cnf.extend(card.clauses)
            nv = card.nv

# only one number can be filled in each cell
for i in range(2*(K**2)):
    for j in range(K**2):
        card = pysat.card.CardEnc.equals(lits=V[i][j], top_id=nv, bound=1, encoding=0)
        cnf.extend(card.clauses)
        nv = card.nv

# corresponding cells of the two sudoku can't be same
for i in range(K**2):
    for j in range(K**2):
        for v in range(K**2):
            card = pysat.card.CardEnc.atmost(lits=[V[i][j][v],V[i+K**2][j][v]], bound=1)
            cnf.extend(card.clauses)

test = Solver(bootstrap_with=cnf.clauses,use_timer=True)
if test.solve():
    solution = [v for v in test.get_model() if v > 0 and v <= 2*((K**2)**3)]
test.add_clause([-v for v in solution])
uncheckedEntries = solution[:]
random.shuffle(uncheckedEntries)
main = []
test.set_phases(v * random.randint(0,1)*2-1 for v in c)
while len(uncheckedEntries):
    important = uncheckedEntries.pop()

    if test.solve(assumptions=main+uncheckedEntries):
        main.append(important)        
    else:
        core = test.get_core()
        uncheckedEntries = [l for l in uncheckedEntries if l in core]
main = set(main)
ans = [[0 for i in range((K**2)**3)] for j in range(2*((K**2)**3))]
for i in range(2*(K**2)):
    for j in range(K**2):
        vs = V[i][j]
        trues = [ix+1 for (ix,v) in enumerate(vs) if v in main]
        if len(trues): 
            ans[i][j] = trues[0]
        else:
            ans[i][j] = 0
with open('output.csv','w') as outputFile:
    for i in range(2*(K**2)):
        for j in range(K**2):
            outputFile.write(str(ans[i][j]))
            if(j!=(K**2-1)):
                outputFile.write(",")
        outputFile.write("\n")
        
