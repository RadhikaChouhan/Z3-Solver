import sys
from z3 import *
from itertools import combinations
inFile = sys.argv[1]
lines = []
with open(inFile,'r') as i:
	lines = i.readlines()
	words = []
	for i in lines:
		i=i.strip()
		words +=i.split(",")

 
n =int ( words[0])
lim = int (words[1])
redx =int ( words[2])
redy = int (words[3])

count = 0
for i in words:
	count+=1

blockh = []
blockv = []
blockr = []
blockm = []
p = []
q = []
r = []
w = []
t = []
v = []

for i in range(n):
	blockh+= [[]]
	blockv+= [[]]
	blockr+= [[]]
	blockm+= [[]]
	p +=[[]]
	q+=[[]]
	r+=[[]]
	w+=[[]]
	t+=[[]]
	v+=[[]]
	for j in range(n):
		blockh[i]+=[[]]
		blockv[i]+=[[]]
		blockr[i]+=[[]]
		p[i]+=[[]]
		q[i]+=[[]]
		r[i]+=[[]]
		w[i]+=[[]]
		t[i]+=[[]]
		v[i]+=[[]]
		
		for k in range(lim+1):
			blockh[i][j] += [Bool("h_%i_%i_%i" % (i,j,k))]
			blockv[i][j] += [Bool("v_%i_%i_%i" % (i,j,k))]
			blockr[i][j] += [Bool("r_%i_%i_%i" % (i,j,k))]
			p[i][j]+= [Bool("p_%i_%i_%i" % (i,j,k))]
			p[i][j][k] = Bool("p[i][j][k]")
			q[i][j]+= [Bool("q_%i_%i_%i" % (i,j,k))]
			r[i][j]+= [Bool("r_%i_%i_%i" % (i,j,k))]
			w[i][j]+= [Bool("s_%i_%i_%i" % (i,j,k))]
			t[i][j]+= [Bool("t_%i_%i_%i" % (i,j,k))]
			v[i][j]+= [Bool("v_%i_%i_%i" % (i,j,k))]
 
		blockm[i] += [Bool("m_%i_%i" % (i,j))]
s= Solver()




blockr[redx][redy][0] = True
s.add(blockr[redx][redy][0])
 
for a in range(count):
 
	if((a%3 == 1) and (a>=4)):
 
		if(words[a] == '0' and a+2<n and a+1<n) :
 
			blockv[int(words[a+1])][int(words[a+2])][0] = True
			s.add(blockv[int(words[a+1])][int(words[a+2])][0])
		elif(words[a] == '1' and a+2<n and a+1<n):
			blockh[int(words[a+1])][int(words[a+2])][0] = True
			s.add(blockh[int(words[a+1])][int(words[a+2])][0])
		elif(words[a] == '2' and a+2<n and a+1<n):
			blockm[int(words[a+1])][int(words[a+2])]= True
			s.add(blockm[int(words[a+1])][int(words[a+2])])
 


def atmost_one(literals):
	c = []
	for pair in combinations(literals,2):
		a,b = pair[0], pair[1]
		c+= [Or(Not(a), Not(b))]
 
	return And(c)

for i in range(n):
	for j in range(n):
		for k in range(lim+1):
			list1 = []
			list1.append(blockh[i][j][k])
			list1.append(blockv[i][j][k])
			list1.append(blockr[i][j][k])
			list1.append(blockm[i][j])
			s.add(atmost_one(list1))



for i in range(n):
	for j in range(n):
		for k in range(lim):
# #moving_right
			if((i==0) and (j>=2)):
				s.add(And( Not(blockm[i][j]),Not(blockr[i][j][k]),Not(blockh[i][j][k]),blockh[i][j-2][k],Not(blockh[i][j-1][k]),Not(blockh[i][j-2][k+1]),blockh[i][j-1][k+1],Not(blockv[i][j][k]))==p[i][j][k] )
			elif(j>=2):
				s.add(And(Not(blockm[i][j]),Not(blockr[i][j][k]),Not(blockh[i][j][k]),blockh[i][j-2][k],Not(blockh[i][j-1][k]),Not(blockh[i][j-2][k+1]),blockh[i][j-1][k+1],Not(blockv[i][j][k]),Not(blockv[i-1][j][k]))==p[i][j][k] )
 
#moving left
			if((i==0) and (j==0)):
				s.add(And(Not(blockm[i][j]),blockh[i][j+1][k],Not(blockh[i][j][k]),Not(blockh[i][j+1][k+1]),blockh[i][j][k+1],Not(blockv[i][j][k]))==q[i][j][k])
			elif((i==0) and (j<=n-3)):
				s.add(And(Not(blockm[i][j]),Not(blockr[i][j-1][k]),Not(blockh[i][j-1][k]),blockh[i][j+1][k],Not(blockh[i][j][k]),Not(blockh[i][j+1][k+1]),blockh[i][j][k+1],Not(blockv[i][j][k]))==q[i][j][k])
 
			elif(j==0):
				s.add(And(Not(blockm[i][j]),False,False,blockh[i][j+1][k],Not(blockh[i][j][k]),Not(blockh[i][j+1][k+1]),blockh[i][j][k+1],Not(blockv[i][j][k]),Not(blockv[i-1][j][k]))==q[i][j][k])
 
			elif( j<= n-3):
				s.add(And(Not(blockm[i][j]),Not(blockr[i][j-1][k]),Not(blockh[i][j-1][k]),blockh[i][j+1][k],Not(blockh[i][j][k]),Not(blockh[i][j+1][k+1]),blockh[i][j][k+1],Not(blockv[i][j][k]),Not(blockv[i-1][j][k]))==q[i][j][k])
 # moving down 

			if((i>=2) and (j==0)):
				s.add(And(Not(blockm[i][j]),Not(blockr[i][j][k]),Not(blockh[i][j][k]),Not(blockv[i][j][k]),Not(blockv[i-1][j][k]),Not(blockv[i-2][j][k+1]),blockv[i-2][j][k],blockv[i-1][j][k+1])==r[i][j][k])
			elif(i>=2):
				s.add(And(Not(blockm[i][j]),Not(blockr[i][j][k]),Not(blockr[i][j-1][k]),Not(blockh[i][j][k]),Not(blockh[i][j-1][k]),Not(blockv[i][j][k]),Not(blockv[i-1][j][k]),Not(blockv[i-2][j][k+1]),blockv[i-2][j][k],blockv[i-1][j][k+1])==r[i][j][k])
#moving up
			if((i==0) and (j==0)):
				s.add(And(Not(blockm[i][j]),Not(blockr[i][j][k]),Not(blockh[i][j][k]),Not(blockv[i][j][k]),Not(blockv[i+1][j][k+1]),blockv[i+1][j][k],blockv[i][j][k+1])==w[i][j][k])
			elif((i==0)):
				s.add(And(Not(blockm[i][j]),Not(blockr[i][j][k]),Not(blockr[i][j-1][k]),Not(blockh[i][j][k]),Not(blockh[i][j-1][k]),Not(blockv[i][j][k]),Not(blockv[i+1][j][k+1]),blockv[i+1][j][k],blockv[i][j][k+1])==w[i][j][k])
			elif((j==0) and (i<=n-3)):
				s.add(And(Not(blockm[i][j]),Not(blockr[i][j][k]),Not(blockh[i][j][k]),Not(blockv[i][j][k]),Not(blockv[i-1][j][k]),Not(blockv[i+1][j][k+1]),blockv[i+1][j][k],blockv[i][j][k+1])==w[i][j][k])
			elif(i<=n-3):
				s.add(And(Not(blockm[i][j]),Not(blockr[i][j][k]),Not(blockr[i][j-1][k]),Not(blockh[i][j][k]),Not(blockh[i][j-1][k]),Not(blockv[i][j][k]),Not(blockv[i-1][j][k]),Not(blockv[i+1][j][k+1]),blockv[i+1][j][k],blockv[i][j][k+1])==w[i][j][k])
#moving_right
			if((i==0) and (j>=2)):
				s.add(And(Not(blockm[i][j]),Not(blockh[i][j][k]),Not(blockv[i][j][k]),blockr[i][j-2][k],blockr[i][j-1][k+1])==t[i][j][k])
			elif(j>=2):
				s.add(And(Not(blockm[i][j]),Not(blockh[i][j][k]),Not(blockv[i][j][k]),blockr[i][j-2][k],Not(blockv[i-1][j][k]),blockr[i][j-1][k+1])==t[i][j][k])
#moving left
			if((i==0) and (j==0)):
				s.add(And(Not(blockm[i][j]),Not(blockv[i][j][k]),blockr[i][j+1][k],blockr[i][j][k+1])==v[i][j][k])
			elif((i==0) and (j<=n-3)):
				s.add(And(Not(blockm[i][j]),Not(blockh[i][j-1][k]),Not(blockv[i][j][k]),blockr[i][j+1][k],blockr[i][j][k+1])==v[i][j][k])
			elif(j==0):
				s.add(And(Not(blockm[i][j]),Not(blockv[i][j][k]),blockr[i][j+1][k],Not(blockv[i-1][j][k]), blockr[i][j][k+1])==v[i][j][k])
			elif( j<= n-3):
				s.add(And(Not(blockm[i][j]),Not(blockh[i][j-1][k]),Not(blockv[i][j][k]),blockr[i][j+1][k],Not(blockv[i-1][j][k]),(blockr[i][j][k+1]))==v[i][j][k])

def exactly_one(literals):
	c=[]
	for pair in combinations(literals,2):
		a,b = pair[0], pair[1]
		c+= [Or(Not(a), Not(b))]
	c+= [Or(literals)]
	return And(c)


def atleast_one(literals):
	c = []
	
	c+= [Or(literals)]
	return Or(c)

lis = []
for k in range(lim+1):
		li = []
		for i in range(n):
			for j in range(n):
				li.append(p[i][j][k])
				li.append(q[i][j][k])
				li.append(r[i][j][k])
				li.append(w[i][j][k])
				li.append(t[i][j][k])
				li.append(v[i][j][k])
				lis.append(p[i][j][k])
				lis.append(q[i][j][k])
				lis.append(r[i][j][k])
				lis.append(w[i][j][k])
				lis.append(t[i][j][k])
				lis.append(v[i][j][k])
		s.add(exactly_one(li))

list = []
for k in range(lim+1):
	 list.append(blockr[redx][n-2][k])
	 
s.add(atleast_one(list))
def print_solution(model,lits):
	for k in range(lim+1):
		for i in range(n):
			for j in range(n):
				if(j==n-2):
					
					if model.evaluate(t[i][j][k]):
						print(i,",",j-1)
						return
					if model.evaluate(v[i][j][k]):
						print(i,",",j+1)
						return
					
					
				if model.evaluate(p[i][j][k]):
						print(i,",",j-1)
						
				if model.evaluate(q[i][j][k]):
						print(i,",",j+1)
						
				if model.evaluate(r[i][j][k]): #down
						print(i-1,",",j)
						
				if model.evaluate(w[i][j][k]):
						print(i+1,",",j)
						
				if model.evaluate(t[i][j][k]):
						print(i,",",j-1)
						
				if model.evaluate(v[i][j][k]):
						print(i,",",j+1)
						

if (str(s.check() )== 'sat'):
	lis = []
	for k in range(lim+1):
		for i in range(n):
			for j in range(n):
				lis.append(p[i][j][k])
				lis.append(q[i][j][k])
				lis.append(r[i][j][k])
				lis.append(w[i][j][k])
				lis.append(t[i][j][k])
				lis.append(v[i][j][k])
				lis.append(blockr[i][j][k])
				

	
	print_solution(s.model(),lis)
