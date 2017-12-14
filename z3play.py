from z3 import *

def bitsum(values, n, stop):
	#ensure uniq and in range
	#TLDR: ( total |= 1<<x ) for x in values
	f = lambda a,x: a|(BitVecVal(1,n+1) << ZeroExt(n+1 - n.bit_length(), values[x])) 
	return reduce(f,range(stop),BitVecVal(0,n+1))

def findLabel(edges, nodes):
	#assumes edges form a valid tree,
	# nodes are numbered 0 to n,
	# and the edges are oriented so that every node is a source or sinc
	#  but not both.
	n = len(edges)
	edges = [nodes[l]-nodes[r] for l,r in edges]
	return And(bitsum(nodes,n,n+1) == ((1<<(n+1))-1), bitsum(edges,n,n) == ((1<<(n+1))-2))

def isTree(edges):
	#checks the assumptions of findlabel
	


n = 4
v = [BitVecVal(x,n.bit_length()) for x in [0,1,2,3,4]]
nodes = Array('a',BitVecSort(n.bit_length()),BitVecSort(n.bit_length()))
clause = findLabel([(v[0],v[1]),(v[0],v[2]),(v[0],v[3]),(v[0],v[4])],nodes)

s = Solver()
s.add(clause)
s.check()
print s.model()[nodes]

#exists x: And(istree(x),
#				Forall(nodes[n1,n2,...,nn], 
#						Not(findLabel(x,nodes))) 