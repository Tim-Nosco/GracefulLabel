from z3 import *

def findLabel(edges, nodes):
	#assumes edges form a valid tree,
	# nodes are numbered 0 to n,
	# and the edges are oriented so that every node is a source or sinc
	#  but not both.
	def bitsum(values, n, stop):
		#ensure uniq and in range
		#TLDR: ( total |= 1<<x ) for x in values
		f = lambda a,x: a|(BitVecVal(1,n+1) << ZeroExt(n+1 - values[x].size(), values[x])) 
		return reduce(f,range(stop),BitVecVal(0,n+1))

	n = len(edges)
	edges = [nodes[l]-nodes[r] for l,r in edges]
	return And(bitsum(nodes,n,n+1) == ((1<<(n+1))-1), bitsum(edges,n,n) == ((1<<(n+1))-2))

def isTree(edges):
	# return True
	n= len(edges)
	left = Function("left",BitVecSort(n.bit_length()),BoolSort())
	right = Function("right",BitVecSort(n.bit_length()),BoolSort())
	clauses = []
	x = BitVec('x',n.bit_length())
	clauses.append(ForAll(x,And(Implies(left(x), Not(right(x))),
								Implies(right(x),Not(left(x))))))
	for l,r in edges:
		clauses.append(left(l))
		clauses.append(right(r))
	return And(*clauses)

def testGraphs(n):
	edges = [(BitVec("el{}".format(i),n.bit_length()),BitVec("er{}".format(i),n.bit_length())) for i in range(n)]
	nodes = Array('nodes',BitVecSort(n.bit_length()),BitVecSort(n.bit_length()))

	s = Solver()

	for (l,r) in edges:
		s.add(ULE(l,n))
		s.add(ULE(r,n))
		s.add(UGT(nodes[l],nodes[r]))

	s.add(isTree(edges))

	s.add( findLabel(edges,nodes) )

	print s
	if s.check()==sat:
		print "SAT"
		m = s.model()
		print m
	else:
		print "UNSAT:"
		print s.unsat_core()

if __name__ == '__main__':
	for n in range(4,1000):
		print "n={}".format(n)
		testGraphs(n)