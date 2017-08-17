# Mosek can be found at mosek.com
from mosek.fusion import *
from itertools import product
import sys
import numpy as np

def generateMonomials(d):
	tot = 0
	monos = {}
	for a,b,c in product(range(d+1), repeat=3):
		if a + b + c == d:
			monos[tot] = (a,b,c)
			tot += 1
	return monos

def evaluateMonomials(monos, d, m, y):
	coeffs = range(len(monos))
	for n in monos:
		a,b,c = monos[n]
		coeffs[n] = (d**a) * (m**b) * (y**c)
	return coeffs

def findWeights(coeffs):
	l = len(coeffs)
	with Model() as M:
		s1 = M.variable(l, Domain.binary())
		s2 = M.variable(l, Domain.binary())
		M.constraint(Expr.dot(Expr.sub(s1,s2),coeffs), Domain.equalsTo(0))
		M.constraint(Expr.add(s1,s2), Domain.lessThan(1))
		M.constraint(Expr.sum(s1), Domain.greaterThan(1))
		M.objective(ObjectiveSense.Minimize, Expr.add(Expr.sum(s1), Expr.sum(s2)))
		M.setSolverParam("mioTolAbsRelaxInt", 1e-8)
		#M.setLogHandler(sys.stdout)
		M.solve()
		if M.getProblemStatus(SolutionType.Integer) == ProblemStatus.PrimalFeasible:
			return np.where(s1.level() > 0.5), np.where(s2.level() > 0.5)
		else:
			return None, None

def makePow(s, e):
	if e==0:
		return ""
	elif e==1:
		return s
	else:
		return "{0}^{1}".format(s,e)

def makeEq(p, monos):
	st = []
	for i in p:
		a,b,c = monos[i]
		st.append(makePow("d",a)+makePow("m",b)+makePow("y",c))
	return " + ".join(st)

def computeInt(p, monos, d, m, y):
	return sum((d**monos[i][0])*(m**monos[i][1])*(y**monos[i][2]) for i in p)

def tryMaxDeg(d, m, y, limit):
	for deg in range(1, limit+1):
		monos = generateMonomials(deg)
		coeffs = evaluateMonomials(monos, d, m, y)
		pos, neg = findWeights(coeffs)
		if pos is not None:
			pos, neg = pos[0], neg[0]
			if computeInt(pos, monos, d, m, y) == computeInt(neg, monos, d, m, y):
				return "{0} = {1}".format(makeEq(pos,monos), makeEq(neg,monos)), deg
	return "?", "?"


def allYear(y, maxDeg):
	mrange = range(1,13)
	drange = { 1: range(1,32),
			   2: range(1,29),
			   3: range(1,32),
			   4: range(1,31),
			   5: range(1,32),
			   6: range(1,31),
			   7: range(1,32),
			   8: range(1,32),
			   9: range(1,31),
			   10: range(1,32),
			   11: range(1,31),
			   12: range(1,32) }

	text = '\\begin{longtable}{lll} d/m/y & degree & polynomial \\\\ \n'

	for m in mrange:
		for d in drange[m]:
			res, deg = tryMaxDeg(d,m,y,maxDeg)
			text += "{0}/{1}/{2} & ${3}$ & ${4}$\\\\ \n".format(d,m,y,deg,res)
			print "{0}/{1}/{2} {3} {4}".format(d,m,y,deg,res)
	text += '\\end{longtable}\n'

	return text


# A minimal polynomial for a single date
d, m, y, maxDeg = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
poly, deg = tryMaxDeg(d, m, y, maxDeg)
print poly

# A full year in LaTeX
#with open("year"+str(17), "w") as file:
#	file.write(allYear(17, maxDeg))

