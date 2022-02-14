import itertools
import pysat
from pysat.solvers import Solver
from pysat.card import *
from pysat.formula import CNF
import csv
cnf=CNF()
k = input()
k = int(k)
def sudoku_rules():
    global cnf
    for r in range(0,2*k*k):
        for c in range(0,k*k):
            number=([int("%d" % (r*(k*k*k*k)+ c*(k*k)+ n+1)) for n in range(0, k*k)])
            card = pysat.card.CardEnc.equals(lits=number, bound=1, encoding=0)
            cnf.extend(card.clauses)

    for r in range(0, 2*k*k):
        for n in range(0, k*k):
            column=([int("%d" % (r*(k*k*k*k)+ c*(k*k)+ n+1)) for c in range(0, k*k)])
            card = pysat.card.CardEnc.equals(lits=column, bound=1, encoding=0)
            cnf.extend(card.clauses)
      
    for c in range(0, k*k):
        for n in range(0, k*k):
            row=([int("%d" % (r*(k*k*k*k)+ c*(k*k)+ n+1)) for r in range(0, k*k)])
            row1=([int("%d" % (r*(k*k*k*k)+ c*(k*k)+ n+1)) for r in range(k*k,2*k*k)])
            card = pysat.card.CardEnc.equals(lits=row, bound=1, encoding=0)
            cnf.extend(card.clauses)
            card = pysat.card.CardEnc.equals(lits=row1, bound=1, encoding=0)
            cnf.extend(card.clauses)

    for startRow in range(0,2*k*k):
        for startCol in range(0,k*k):
            if((startRow%k==0)&(startCol%k==0)) :
                for n in range(0, k*k):
                    block=([int("%d" % ((startRow + deltaRow)*(k*k*k*k)+ (startCol + deltaCol)*(k*k)+ n+1))
                    for deltaRow, deltaCol in itertools.product(range(0, k), repeat=2)])
                    card = pysat.card.CardEnc.equals(lits=block,bound=1,encoding=0)
                    cnf.extend(card.clauses)
    for r in range(0,k*k):
        for c in range(0,k*k):
            for n in range(0,k*k):
                corresponding= [r*k**4+c*k**2+n+1,k**6+r*k**4+c*k**2+n+1]
                card = pysat.card.CardEnc.atmost(lits=corresponding,bound=1,encoding=0)
                cnf.extend(card.clauses)  
    return cnf

def given(fname):
    literals = []
    with open(fname, 'r') as fin:
        lines=fin.readlines()
        for l in lines:
            for c in l.split(','):
                if(int(c) != 0):
                    literals.append((lines.index(l))*(k*k*k*k)+(l.split(',').index(c))*(k*k)+int(c))
    return literals

def add_given(solver, literals):
    for l in literals:
        solver.add_clause([l])

cnf=sudoku_rules()
solver = Solver(bootstrap_with=cnf.clauses,use_timer=True)
sudoku = given("./input.csv")
add_given(solver, sudoku)
result = solver.solve()
# print(solver.time())
if result == False:
    print("NONE")
elif result == True:
    model = solver.get_model()
    rows, cols = (2*k*k, k*k)
    ans = [[0 for i in range(0,cols)] for j in range(0,rows)]
    for x in model:
        if(x>0):
            y=int(x-1)
            z = y-int(y%(k*k*k*k))
            ans[int(y/(k*k*k*k))][int((y%(k*k*k*k))/(k*k))] = int(y%(k*k)+1)
    print("SUDOKU-1\n")
    for i in range (0,2*k*k):
        for j in range (0,k*k):
            print(ans[i][j],end=" ")
        print("\n")
        if (i==k*k-1): 
            print("SUDOKU-2\n")