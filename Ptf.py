import networkx as net
import matplotlib.pyplot as plt

def SinL(S,L):#Una lista dentro de otra lista
	flag = True	
	for j in S:
		if j not in L:
			flag = False
			break			
	return flag
	
def SinL2(S,L):#Lista S dentro de una lista de listas L
	i =0
	while i < len(L):
		if SinL(S,L[i]):
			break
		else:
			i+=1
	if i==len(L):
		return False
	else:
		return True
		
def SmenosW(S,W):
	Result=[]
	for i in S:
		if i not in W:
			Result.append(i)
	return Result

def M(G,v,colores):
	S=[]
	Colors=[]
	for i in range(len(G)):
		if i!=v:
			S.append(i)
	L=[]
	l=[]
	for i in range(len(G)):
		if i!=v:
			l.append(i)		
	L.append(l)
	
	Z=[]
	Z.append(v)
	Zs=[]	
	Zs.append(Z)
		
	while SinL2(S,L) and Zs!=[]:
		for i in S:
			for j in L:
				for k in j:
					if k ==i:
						j.remove(k)
		for j in L:
			if j ==[]:
				L.remove(j)
		
		P=[]  #Particion por colores de S con respecto a Zs[0][0] (w en el algoritmo)
		for i in range(colores+1):
			l=[]
			P.append(l)
	
		for i in S:			
			P[G[Zs[0][0]][i]].append(i)
				
		for W in P:
			if W != []:
				if W not in L:
					L.append(W)
				ZW=[]
				ZW.append(SmenosW(S,W))
				ZW.append(Zs[0][1:])
				
				for i in ZW:
					if i not in Zs and i !=[]:
						Zs.append(i)
				
		S=[]
		if len(L)>=1:
			for i in L[0]:
				S.append(i)
			
		Zs=Zs[1:]
	for l in L:
		Colors.append(G[v][l[0]])
	return L,Colors

def gv(G,N): #Construye un subgrafo de G que contiene solamente los nodos en N
	Graph =[]
	for i in N:
		l =[]
		for j in N:
			l.append(G[i][j])
		Graph.append(l)
	return Graph	

def Gv(G,n,N): #Grafo dirigido sin bucles, 
	GResult=[]
	for j in range(len(G)):
		if j!=n:
			l=[]
			l.append(N[j])
			ColorToN =G[j][n]
			for i in range(len(G[j])):
				if G[j][i]!= ColorToN and G[j][i]!=0:
					flag =True
					for k in GResult:
						if i in k:
							flag=False
					if flag:
						l.append(N[i])
			GResult.append(l)
	return GResult #Lista de listas. El primer elemento de cada lista es el nodo que conecta con los siguientes elementos de su lista
	
def sink(G):
	sink=[]
	found= False
	i=0
	while i < len(G) and not found:
		if len(G[i])==1:
			sink = G[i]
			found = True
		else:
			i+=1
	return sink

def CalculaF(Sink,Partition):#m y P en el programa ptf. Devuelve una lista con los miembros del sink segun se encuentren en M(g,v) 
	MembersInSink=[]
	for i in range(len(Sink)):
		ItIsHere = False		
		while not ItIsHere:
			for j in Partition:
				if Sink[i] in j:						
					ItIsHere =True
					if j not in MembersInSink:
						MembersInSink.append(j)
	return MembersInSink
  
def ptf(G,v,c):
	Nodes=[]
	Edges=[]
	P=M(G,v,c)	
	N=[]
	N.append(v)
	for i in P:
		N.append(i[0])
	N.sort()
	g=gv(G,N)#g'
	gnb=Gv(g,v,N)#devuelve G''
	Nodes.append('t')
	u ='t'
	Type=''
	while gnb!=[]:
		Nodes.append('w')
		Edges.append([u,'w'])
		m=sink(gnb)		
		if m !=[]:
			F=CalculaF(m,P)
			for i in gnb:	
				if m[0] in i:
					i.remove(m[0])
				if i ==[]:
					gnb.remove(i)
			
			if len(F)>1:
				Type='primitive'							
			else:
				Type='complete'
			for i in F:	
				ptf_i = ptf(gv(G,i),0,c)	
					
				if Type == ptf_i[0]== 'complete': # and both have the same color?
					for k in ptf_i[1][1:]:
						if 't' not in str(k) and 'w' not in str(k):
							Nodes.append(i[k])
						else:
							Nodes.append(k+str(i[0]))
												
					for k in ptf_i[2][1:]:		
						NodesInEdge_ptf=[]
						for j in k:						
							if 't' not in str(j) and 'w' not in str(j):
								NodesInEdge_ptf.append(i[j])
							elif 'w' in str(j):
								NodesInEdge_ptf.append(j+str(i[0]))								
						if len(NodesInEdge)==2:
							Edges.append(NodesInEdge_ptf)
						if 'w' in str(NodesInEdge_ptf[0]):
							Edges.append([u,NodesInEdge_ptf[0]])
            
					if 't' not in str(ptf_i[2][1][0]) and 'w' not in str(ptf_i[2][1][0]):
						Edges.append([u,i[ptf_i[2][1][0]]])
					elif 'w' in str(ptf_i[2][1][0]):
						Edges.append([u,ptf_i[2][1][0]+str(i[0])])
						
				else:
					for k in ptf_i[1]:
						if 't' not in str(k) and 'w' not in str(k):
							Nodes.append(i[k])
						else:
							Nodes.append(k+str(i[0]))
							
					for k in ptf_i[2]:		
						NodeInEdge_ptf=[]
						for j in k:
							if 't' not in str(j) and 'w' not in str(j):
								NodeInEdge_ptf.append(i[j])
							else:
								NodeInEdge_ptf.append(j+str(i[0]))				
						Edges.append(NodeInEdge_ptf)
									
					if 't' not in str(ptf_i[2][0][0]) and 'w' not in str(ptf_i[2][0][0]):
						Edges.append([u,i[ptf_i[2][0][0]]])
					else:
						Edges.append([u,ptf_i[2][0][0]+str(i[0])])#+str(i))
								
			u='w'
	Nodes.append(v)
	Edges.appende(['w',v])
	return (Type,Nodes,Edges)

def DrawPtf(Nodes,Edges):
	G = net.Graph()
	G.add_nodes_from(Nodes)
	G.add_edges_from(Edges)
	net.draw_spectral(G,node_color='k')
	#net.draw_circular(G,node_color='k')
	plt.show()
	
#G1=[[0,1,1,2,2],[1,0,1,2,2],[1,1,0,2,2],[2,2,2,0,2],[2,2,2,2,0]]	
#primetreefam= ptf(G1,0,2)
#print "Nodos:", primetreefam[1]
#print "Aristas:", primetreefam[2]
#DrawPtf(primetreefam[1],primetreefam[2])
