import unittest

def isTree(tree):
	#tree is a list of n tuples
	n = len(tree)
	left = set()
	right = set()
	both = set()
	for l,r in tree:
		left.add(l)
		right.add(r)
		both.update([l,r])
	#must be connected (n+1 distinct verticies)
	if len(both)!=n+1:
		return False
	#every node must be a source or a sinc but not both
	if left.intersection(right):
		return False
	return True

def isGraceful(tree, labeling):
	#ASSUMES: tree is valid
	#tree is a list of n tuples representing a directed tree
	#	where tree=[(l,r)..] and lr is oriented l->r
	#	a valid labeling requires r to be strictly greater than l
	edges = set()
	identity = dict()
	n = len(tree)
	for (l_idenity,r_idenity),(l_value,r_value) in zip(tree,labeling):
		#ensure proper structure
		assumed_l = identity.get(l_idenity,l_value)
		assumed_r = identity.get(r_idenity,r_value)
		if assumed_l != l_value or assumed_r != r_value:
			# print "REUSED value. Assumed: {} Got: {}".format((assumed_l,assumed_r),(l_value,r_value))
			return False
		identity[l_idenity] = assumed_l
		identity[r_idenity] = assumed_r
		#ensure uniqueness and range of edges
		edge = r_value-l_value
		if edge in edges or edge<=0 or edge>n:
			# print "EDGE fail. Value: {} Reused? {}".format(edge,edge in edges)
			return False
		edges.add(edge)
		#ensure range of verticies
		if r_value < 0 or r_value > n or l_value < 0 or l_value > n:
			# print "NODE out of range. l: {} r: {}".format(l_value,r_value)
			return False
	return True

class Test(unittest.TestCase):
	def testg1(self):
		tree = [(0,1),(2,1)]
		labeling = [(1,2),(0,2)]
		self.assertTrue(isGraceful(tree,labeling))
	def testg2(self):
		tree = [(0,1),(2,1)]
		labeling = [(1,0),(2,0)]
		self.assertFalse(isGraceful(tree,labeling))

if __name__ == '__main__':
	unittest.main()
	# from z3 import *
	# s = Solver()
	# s.add(Forall(x,Implies(isTree(x),
	# 			something)))