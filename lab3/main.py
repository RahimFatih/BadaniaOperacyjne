import numpy as np
from random import randint 
import time
def load_graph(pathToFile):
  with open(pathToFile,'r') as file:
    return(np.loadtxt(file))


def dfs(visited, graph, node):  
  if node not in visited:
      visited.add(node)
      i=0
      for neighbour in graph[node]:
        if neighbour>0:
          dfs(visited, graph, i)
        i=i+1 
  return(visited) 
def BFS(graph, start, end, path_to_node):
    visited = [0]*(len(graph))
    queue = []
    queue.append(start)
    visited[start] = True
    while queue:
        u = queue.pop(0)

        for ind, val in enumerate(graph[u]):
            if visited[ind] == False and val > 0:
                queue.append(ind)
                visited[ind] = True
                path_to_node[ind] = u
                if ind == end:
                    return True
    return False
def check_end_start_connection(graph, node):
  visited = set() #
  dfs(visited,graph,node)
  return(len(graph)-1 in visited)
#Funkcja do przeszukiwania grafu pod kątem sciezek przepływowych
class Solution:
    def __init__(self):
        self.flag = False
def dfs_for_ff(visited,graph,node,act_flow,residual_flow,path):
  #print("odwiedzone ",visited)
  #print("sciezka ",path)
  #print("aktualny ",node)
  target_path=np.array([])
  if (node not in visited):
    path=np.append(path,node)
    visited.add(node)
    if node==(len(graph)-1) :
      target_path=np.copy(path)
      print("sciezka zwracana ",target_path)
      return(target_path)
    
    for ind,neighbour_cap in enumerate(graph[node]):
      if ((graph[node][ind]-act_flow[node][ind])>0 or (0-residual_flow[node][ind]>0) ):
        dfs_for_ff(visited,graph,ind,act_flow,residual_flow,path)
  if target_path.size>0:
    return(target_path)
  else:
    return()

def update_flows(augmentable_path):
  bottlneck=99999
  for path_id in range(len(augmentable_path)-1):
    if graph[augmentable_path[path_id]][augmentable_path[path_id+1]]>0:
      path_capacity = graph[augmentable_path[path_id]][augmentable_path[path_id+1]]-actfl[augmentable_path[path_id]][augmentable_path[path_id+1]]
     

def ford_fulkerson_z_zapamietywaniem(graph):
  act_flow=np.zeros((len(graph),len(graph)))
  residual_flow=np.copy(act_flow)
  visited = set()
  path=np.array([])
  parrent_array=np.zeros(len(graph))
  augmentable_path=dfs_for_ff(visited,graph,0,act_flow,residual_flow,path)
  print(augmentable_path)
  bottlneck=99999
  for path_id in range(len(augmentable_path)-1):
   if graph[augmentable_path[path_id]][augmentable_path[path_id+1]]>0:
     path_capacity = graph[augmentable_path[path_id]][augmentable_path[path_id+1]]-act_flow[augmentable_path[path_id]][augmentable_path[path_id+1]]





def ford_fulkerson_bez_zapamietywania(graph,source, sink):
    path_to_node = [-1]*(len(graph))
    sum_of_bottlnecks = 0 
    #Wykonuj algorytm dopoki istnieje poprawialna sciezka
    while BFS(graph,source, sink, path_to_node) :

        bottleneck = 9999999
        s = sink
        while(s !=  source):
            bottleneck = min (bottleneck, graph[path_to_node[s]][s])
            s = path_to_node[s]
        sum_of_bottlnecks +=  bottleneck

        v = sink
        while(v !=  source):
            u = path_to_node[v]
            graph[u][v] -= bottleneck
            graph[v][u] += bottleneck
            v = path_to_node[v]
    return sum_of_bottlnecks
def gencoordinates(m, n):
    seen = set()

    x, y = randint(m, n), randint(m, n)

    while True:
        seen.add((x, y))
        yield (x, y)
        x, y = randint(m, n), randint(m, n)
        while (x, y) in seen:
            x, y = randint(m, n), randint(m, n)

def generateGraph(nodes,paths):
  graph=np.random.rand(nodes,nodes)
  graph=(np.rint(graph*100)).astype(int) 
  for i in range(len(graph)):
    graph[i][i]=0
  numbers=list(range(nodes))
  gen = gencoordinates(0,nodes-1)
  for i in range(int(nodes*nodes-paths)): 
    pair = next(gen)
    graph[pair[0]][pair[1]]=0
  
  return(graph)
  
#Kod poniżej służył do sprawdzenia czy algorytm działa poprawnie 
#graph = load_graph("data.txt")
#print (ford_fulkerson_bez_zapamietywania(graph,0,len(graph)-1))
print("Nodes,Paths,Time,GenerationTime")
for i in range(100,500):
  start_generating=time.time()
  graph=generateGraph(i,5000)
  generating_time=time.time()-start_generating
  start_time=time.time()
  ford_fulkerson_bez_zapamietywania(graph,0,len(graph)-1)
  elapsed_time=time.time()-start_time
  print(i,",",np.count_nonzero(graph),",",elapsed_time,",",generating_time)
print("Nodes,Paths,Time,GenerationTime")
for i in range(1000,80000,1000):
  start_generating=time.time()
  graph=generateGraph(300,i)
  generating_time=time.time()-start_generating
  start_time=time.time()
  ford_fulkerson_bez_zapamietywania(graph,0,len(graph)-1)
  elapsed_time=time.time()-start_time
  print(300,",",np.count_nonzero(graph),",",elapsed_time,",",generating_time)