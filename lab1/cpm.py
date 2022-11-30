
import random
import numpy
import time

class Task:
    def __init__(self,name,time):
        self.name=name
        self.time=time
        self.ES=-1
        self.EF=time
        self.LS=-1
        self.LF=-1
        self.TF=0
        self.critical_path=[]


class CPMAlgorithm:
    def __init__(self) -> None:
        self.task_list=[]
        self.task_connections=[]
        self.max=0
        pass
    def import_data(self,path):
        with open(path) as file:
            mylist = file.read().splitlines()
            N,M=mylist[0].split(" ")
            tasks=mylist[1].split(" ")
            
            for count, task in enumerate(tasks):
                self.task_list.append(Task(count,int(task)))
            for connection in mylist[2].split("  "):
                self.task_connections.append([int(x) - 1 for x in connection.split(" ")])
            
            self.task_connections=sorted(self.task_connections, key=lambda x: (x[0], x[1]))
            

    def calculate_ELFS(self):
        change_flag=True
        cycle_counter=0
        while change_flag:
            change_flag=False
            for connection in self.task_connections:
                if self.task_list[connection[1]].EF < self.task_list[connection[0]].EF + self.task_list[connection[1]].time:
                    change_flag=True
                    self.task_list[connection[1]].EF=self.task_list[connection[0]].EF+self.task_list[connection[1]].time 
            cycle_counter=cycle_counter+1
            if(cycle_counter==len(self.task_list)):
                raise Exception("W grafie znajduje się cykl")
        self.max=max(self.task_list,key=lambda x: x.EF).EF
        for task in self.task_list:
            task.ES = task.EF-task.time
            task.LF = self.max
        change_flag=True
        while change_flag:
            change_flag = False
            for connection in self.task_connections:
                if self.task_list[connection[0]].LF > self.task_list[connection[1]].LF - self.task_list[connection[1]].time:
                    change_flag = True
                    self.task_list[connection[0]].LF = self.task_list[connection[1]].LF - self.task_list[connection[1]].time
        for task in self.task_list:
            task.LS=task.LF - task.time
            task.TF=task.LS-task.ES
        critical_tasks = list(filter(lambda x: x.TF == 0,self.task_list))
        critical_path=[]
        critical_path.append(max(critical_tasks,key=lambda x: x.EF))
        #print("-----------------------------",critical_path[-1].name)
        while True:
            critical_task_EF=0
            critical_task=0
            for connection in list(filter(lambda x:x[1]==critical_path[-1].name,self.task_connections)):
                if self.task_list[connection[0]].EF>critical_task_EF:
                    critical_task=self.task_list[connection[0]]
                    critical_task_EF=critical_task.EF
            if critical_task!=0:
                critical_path.append(critical_task)
            if critical_path[-1].ES==0:
                self.critical_path=critical_path
                break
        
    def print_ELFS(self):
        for task in self.task_list:
            print("Name: "+str(task.name)+"   ES: ",task.ES, " EF: ", task.EF, " LS: ", task.LS, " LF: ", task.LF, " TF: ",task.TF  )

        print("Max: ",self.max)
        path="Critical path: start"
    
        for task in self.critical_path[::-1]:
            path=path +"->"+ str(task.name)
        print(path)

class data_generator:
    def __init__(self,n,m,mixer) -> None:
        self.n=n
        self.m=m
        self.connection_list=[]
        self.times=[]
        connections=numpy.zeros([n,n],int)
        for i in range(self.n):
            self.times.append(str(random.randint(1,100)))
        for i in range(self.m):
            while True:
                a=random.randint(0,n-2)
                b=random.randint(a+1,n-1)
                if connections[a, b]==0:
                    connections[a,b]=1
                    break

        for i in range(mixer):
            a=random.randint(0,n-1)
            b=random.randint(0,n-1)
            connections[:, [b, a]] = connections[:, [a, b]]
            connections[[a, b]] = connections[[b, a]]
        for i in range(n):
            for j in range(n):
                if connections[i,j]==1:
                    self.connection_list.append(str(i)+' '+str(j))
        pass
    def import_to_file(self,file_name):
        with open(file_name, 'w') as the_file:
            the_file.write(str(self.n)+" "+str(self.m)+'\n')
            the_file.write(' '.join(self.times)+'\n')
            the_file.write('  '.join(self.connection_list))
        






if __name__ == "__main__":
    for i in range(2400,4000,50):
        gener=data_generator(2000,i,i)
        gener.import_to_file("test")
        alg=CPMAlgorithm()
        alg.import_data("test")
        start=time.time()
        alg.calculate_ELFS()
        end=time.time()    
        print(i," ",end-start)
