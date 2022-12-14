import numpy as np
import random


def connectionGenerator(n,m):
    connectionMatrix = np.ones((n,n),int)
    for i in range(n):
        for j in range(n):
            connectionMatrix[i][j]=random.randint(1,100) * (random.random()>m)
    return(connectionMatrix)


def Dijkstry(ConnectionMatrix):
    n=len(ConnectionMatrix[0])
    Q=[*range(n)]
    S=[]
    d=np.ones(n,int)*9999999
    d[0]=0
    p=np.ones(n,int)*(-1)

    for i in range(n):
        minD=9999999
        minU=-1
        for u in Q:
            if d[u] < minD:
                minD=d[u]
                minU=u
        S.append(Q.pop(Q.index(minU)))
        for u in range(n):
            if ConnectionMatrix[minU][u]>0:
                if d[u]>d[minU]+ConnectionMatrix[minU][u]:
                    d[u]=d[minU]+ConnectionMatrix[minU][u]
                    p[u]=minU
    path_list=[]
    for i in range(n):
        current_node=i
        path_to_i=[]
        path_to_i.append(i)
        while(p[current_node]!=-1):
            current_node=p[current_node]
            path_to_i.insert(0,current_node)
        path_list.append(path_to_i)
    print(path_list)

    print(d)

def BellmanFord(ConnectionMatrix):
    n=len(ConnectionMatrix[0])
    Q=[*range(n)]#niezrelaksowane
    S=[]#zrelaksowane
    d=np.ones(n,int)*9999999
    d[0]=0
    p=np.ones(n,int)*(-1)
    for relaxation in range(n-1):
        change_flag=0
        for i in range(n):
            for j in range(n):
                if ConnectionMatrix[i][j] !=0:
                    if d[i]+ConnectionMatrix[i][j]<d[j]:
                        d[j]=d[i]+ConnectionMatrix[i][j]
                        p[j]=i
                        change_flag=1
        if change_flag==0:
            break
    print(d)
if __name__ == "__main__":
    with open("./lab2/src/src.txt","r") as file:
        lines = file.readlines()
    n = int(lines[0])
    ConnectionMatrix=np.zeros((n,n),int)
    for i in range(1,n+1):
    #print(lines[i])
        for j in range(1,n+1):
            ConnectionMatrix[i-1][j-1]=int(lines[i].split("  ")[j])
    ConnectionMatrix=connectionGenerator(10,0.5)
    Dijkstry(ConnectionMatrix)
    BellmanFord(ConnectionMatrix)
    


