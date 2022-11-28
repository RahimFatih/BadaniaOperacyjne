
class Task:
    def __init__(self,name,a,m,b):
        self.a=a
        self.m=m
        self.b=b
        self.time=(a+4*m+b)/6
        self.variant=((a-self.time)**2+4*((m-self.time)**2)+(b-self.time)**2)/6
        self.name=name
        self.ES=-1
        self.EF=self.time
        self.LS=-1
        self.LF=-1
        self.TF=0
        self.critical_path=[]



class CPMAlgorithm:
    def __init__(self) -> None:
        self.task_list=[]
        self.task_connections=[]
        self.max=0
        self.project_variant=0
        pass
    def import_data(self,path):
        with open(path) as file:
            mylist = file.read().splitlines()
            N,M=mylist[0].split(" ")
            tasks=mylist[1].split("   ")
            
            for count, task in enumerate(tasks):
                self.task_list.append(Task(count,int(task.split(" ")[0]),int(task.split(" ")[1]),int(task.split(" ")[2])))
            for connection in mylist[2].split("   "):
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
        print("-----------------------------",critical_path[-1].name)
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
        self.project_variant=0
        for task in self.critical_path:
            self.project_variant+=task.variant
    def print_ELFS(self):
        path=""
        for task in self.critical_path[::-1]:
            path=path +" "+ str(task.name)
        print(len(self.critical_path),": ",path)
        print(round(self.max,1)," ",round(self.project_variant,1))
            

        print(path)





if __name__ == "__main__":
    alg=CPMAlgorithm()
    alg.import_data("./lab1/pert_data.txt")
    #alg.print_ELFS()
    alg.calculate_ELFS()
    alg.print_ELFS()