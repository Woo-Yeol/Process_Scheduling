from django.shortcuts import render
from .models import Process,Processor,ReadyQueue

# SPN Scheduling Class 생성
class Spn:
    # 생성자
    def __init__(self,input_value):
        self.process_ls=[]
        self.processor_ls=[]
        self.readyQueue = ReadyQueue()

        self.process_n = int(input_value[0])
        self.processor_n = int(input_value[1])
        self.bt_ls = list(input_value[2])
        self.at_ls = list(input_value[3])

        # 프로세스/프로세서 객체 생성
        for n in range(self.process_n):
            self.process_ls.append(Process(self.bt_ls[n],self.at_ls[n],n))
        for n in range(self.processor_n):
            self.processor_ls.append(Processor())
    
    # SPN 멀티코어 프로세싱
    def mulitcore_processing(self):
        time = 0; terminate = 0
        while(terminate != self.process_n):
            self.readyQueue.readyQue(self.process_ls,time)
            time += 1
            for processor in self.processor_ls:
                # 큐에 프로세스가 있다면 비어있는 프로세서에 할당
                processor.ready_to_running(self.readyQueue)
                # 프로세서에 있는 프로세스 처리하기
                terminate += processor.running_process(time)
        # 출력
        for process in self.process_ls:
            print(str(process))      

# Create your views here.
def index(request):
    example = [15,4,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],[10,3,10,3,10,3,10,3,10,3,10,3,10,3,10]]
    result = Spn(example)
    result.mulitcore_processing()
    return render(request, 'index.html',{'result' : result})