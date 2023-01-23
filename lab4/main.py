import numpy as np
import math
import random
import time


def calc_route_length(graph,route):
    sum=0
    for ind in range(-1,len(route)-1):
        sum+=math.dist(graph[route[ind]],graph[route[ind+1]])
    return(sum)
def opt2(graph,route):
    route_length=len(route)
    improvment=True
    best_route=np.copy(route)
    best_len=calc_route_length(graph,route)
    while(improvment==True):
        improvment=False

        for swapA in range(route_length):
            for swapB in range(swapA+2,route_length+swapA-1):
                new_route=np.copy(route)
                new_route[swapA:swapB+1]=np.flip(route[swapA:swapB+1])
                if(best_len>calc_route_length(graph,new_route)):
                    best_len=calc_route_length(graph,new_route)
                    best_route=np.copy(new_route)
                    improvment=True
        route=np.copy(best_route)
    return(best_len)
def sym_wyzarz(graph,route,t,k,epoch_size):
    route_length=len(route)
    cont=True
    best_route=np.copy(route)
    best_len=calc_route_length(graph,route)
    last_epoch_best_len=best_len
    while(cont==True):
        cont=False
        for i in range(epoch_size):
            new_route=np.copy(best_route)
            swapA=random.randrange(0,route_length,1)
            swapB=(swapA+1)%route_length
            new_route[[swapA,swapB]]=new_route[[swapB,swapA]]
            if(best_len>calc_route_length(graph,new_route)):
                best_len=calc_route_length(graph,new_route)
                best_route=np.copy(new_route)
            else:
                if math.exp((best_len-calc_route_length(graph,new_route))/t)>random.random():
                    best_len=calc_route_length(graph,new_route)
                    best_route=np.copy(new_route)
            #print(best_len)
        t=t*k
        if abs(best_len-last_epoch_best_len)>0.001*best_len:
            cont=True
        last_epoch_best_len=best_len
    return(best_len)
def farthest_verticies(graph):
    max_distance=0
    for i in range(len(graph)):
        for j in range(len(graph)):
            distance=math.dist(graph[i],graph[j])
            if distance>max_distance:
                max_distance=distance
                max_a=i
                max_b=j
    return(int(max_a),int(max_b))
def farthest_vertice_from_route(graph,route):
    max_distance=0
    for i in range(len(graph)):
        if not i in route:
            for j in route:
                distance=math.dist(graph[i],graph[j])
            if distance>max_distance:
                max_distance=distance
                max_i=i
    return(int(max_i))
def find_closest_edge(graph,route,point):
    min_dist=9999999
    for edge in range(-1,len(route)-1):
        x1=graph[route[edge]][0]
        y1=graph[route[edge]][1]
        x2=graph[route[edge+1]][0]
        y2=graph[route[edge+1]][1]
        x0=graph[point][0]
        y0=graph[point][1]
        distance=abs((x2-x1)*(y1-y0)-(x1-x0)*(y2-y1))/(math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2)))
        if distance<min_dist:
            min_dist=distance
            closest_edge=[route[edge],route[edge+1]]
    return(closest_edge)
def farthest_insertion_alg(graph):
    not_routed=[*range(len(graph))]
    route=np.array([],dtype=np.uint32)
    
    farthest=farthest_verticies(graph)
    for x in farthest:
        not_routed.remove(x)
    route=np.append(route,farthest)

    farthest=farthest_vertice_from_route(graph,route)
    route=np.append(route,farthest)
    not_routed.remove(farthest)

    while(len(not_routed)>0):
        farthest=farthest_vertice_from_route(graph,route)
        closes_edge=find_closest_edge(graph,route,farthest)

        route=np.insert(route,np.where(route == closes_edge[1])[0],farthest)

        not_routed.remove(farthest)
    return(calc_route_length(graph,route))
#opt2(graph,route)
def data_generator(n,max):
    return((np.random.rand(n,2)*max).astype(int))

print("n,opt2,wyzyz,farthest")
#wynik1
for i in range(5,1000,5):
    sum_Opt2=0
    sum_Wyzaz=0
    sum_Farthest=0
    for j in range(10):
        data=data_generator(i,1000)
        
        s_time_Opt2=time.time()
        #opt2(data,np.array(range(len(data))))
        e_time_Opt2=time.time()

        s_time_Wyzaz=time.time()
        sym_wyzarz(data,np.array(range(len(data))),100,0.9,len(data))
        e_time_Wyzaz=time.time()

        s_time_Farthest=time.time()
        farthest_insertion_alg(data)
        e_time_Farthest=time.time()

        sum_Opt2+=e_time_Opt2-s_time_Opt2
        sum_Wyzaz+=e_time_Wyzaz-s_time_Wyzaz
        sum_Farthest+=e_time_Farthest-s_time_Farthest
    print(len(data),",",sum_Opt2/10,",",sum_Wyzaz/10,",",sum_Farthest/10)
#wynik2
#for i in range(5,100,1):
#    sum_Opt2=0
#    sum_Wyzaz=0
#    sum_Farthest=0
#    for j in range(10):
#        data=data_generator(i,1000)
#
#
#        sum_Opt2+=opt2(data,np.array(range(len(data))))
#        sum_Wyzaz+=sym_wyzarz(data,np.array(range(len(data))),100,0.9,len(data))
#        sum_Farthest+=farthest_insertion_alg(data)
#
#
#    print(len(data),",",sum_Opt2/10,",",sum_Wyzaz/10,",",sum_Farthest/10)
