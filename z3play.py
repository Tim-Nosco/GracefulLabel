from z3 import *

def findLabel(edges, nodes):
	#assumes edges form a valid tree,
	# nodes are numbered 0 to n,
	# and the edges are oriented so that every node is a source or sinc
	#  but not both.
	def bitsum(n, stop, g):
		#ensure uniq and in range
		#TLDR: ( total |= 1<<x ) for x in values
		f = lambda a,x: a|(BitVecVal(1,n+1) << ZeroExt(n+1 - g(x).size(), g(x))) 
		return reduce(f,range(stop),BitVecVal(0,n+1))

	n = len(edges)
	edges = [nodes(l)-nodes(r) for l,r in edges]
	return And(bitsum(n,n+1,lambda x: nodes(x)) == ((1<<(n+1))-1), 
			   bitsum(n,n,  lambda x: edges[x]) == ((1<<(n+1))-2))

def isTree(edges):
	n= len(edges)
	left = Function("left",BitVecSort(n.bit_length()),BoolSort())
	right = Function("right",BitVecSort(n.bit_length()),BoolSort())
	clauses = []
	x = BitVec('x',n.bit_length())
	a = []
	for l,r in edges:
		clauses.append(left(l))
		clauses.append(right(r))
		a+=[x==l,x==r]

	clauses.append(ForAll(x,Implies(Or(left(x), right(x)),
							Or(*a))))
	for i in range(n+1):
		clauses.append(Xor(left(i),right(i)))
	return And(*clauses)

def testGraphs(n):
	edges = [(BitVec("el{}".format(i),n.bit_length()),BitVec("er{}".format(i),n.bit_length())) for i in range(n)]
	nodes = Function("nodes",BitVecSort(n.bit_length()),BitVecSort(n.bit_length()))

	s = Solver()

	tmp = []
	marriage = []
	for (l,r) in edges:
		s.add(ULE(l,n))
		s.add(ULE(r,n))
		marriage.append(UGT(nodes(l),nodes(r)))
	for i in range(n+1):
		x = BitVec("x{}".format(i),n.bit_length())
		tmp.append(x)
		marriage.append(nodes(i)==x)

	# # s.set(auto_config=False, mbqi=True, macro_finder=True)

	s.add( And( isTree( edges ),
				ForAll( tmp, And( Not(findLabel(edges,nodes)) ,
								  *marriage))))
	# s.add(And(isTree(edges),
	# 		  findLabel(edges,nodes),
	# 		  *marriage))

	# print s
	if s.check()==sat:
		print "SAT"
		m = s.model()
		print m
		print "EDGES:"
		for l,r in edges:
			print "{} => {}".format(m[tmp[m[l].as_long()]],m[tmp[m[r].as_long()]])
	else:
		print "UNSAT"
		# print s.unsat_core()

if __name__ == '__main__':
	for n in range(4,50):
		print "n={}".format(n)
		testGraphs(n)