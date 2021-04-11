# Python list를 이용한 PriorityQueue ADT 구현.
class ReadyQueue:
    # 생성자

    # 비어있는지 확인
    def isEmpty(self) : return len(self.items) == 0
    
    # 큐의 크기 확인
    def size(self): return len(self.items)

    # 큐 초기화
    def clear(self): self.items = []

    # 큐 삽입
    def enqueue(self, item):    # 삽입 연산
        self.items.append(item)
    
    # 최대 우선순위 항목의 인덱스 반환
    def findMaxIndex(self):            
        if self.isEmpty(): return None
        else:
            highest = 0                 # 0번을 최대라고 하고
            for i in range(1, self.size()): # 모든 항목에 대해서
                if self.items[i].bt < self.items[highest].bt:   # Burst Time이 가장 낮으면 가장 높은 우선순위
                    highest = i         # 인덱스 갱신
            return highest

    # 레디 큐 생성 연산
    def readyQue(self,process_ls,time):
        for process in process_ls:
            if (process.at == time):
                self.enqueue(process)

class Nom_ReadyQueue(ReadyQueue):
    def __init__(self):
        self.items = []

    def dequeue(self):
        if not self.isEmpty():
            return self.items.pop(0)

    def peek(self):
        if not self.isEmpty():
            return self.items[0]

# Process Class Declair
class Process:
    def __init__(self,bt,at,n):
        self.bt = int(bt)            # Process Burst Time
        self.r_bt = int(bt)          # Process Burst Time 기억용
        self.at = int(at)            # Process Arrive Time 
        self.tt =  0                 # Process Turnaround Time   반납시간 - At
        self.ntt = 0                 # Nomalized Turnaround Time TT/BT
        self.wt = 0                  # Waiting Time              TT-BT
        self.id = int(n+1)

    def modify_process(self,time):
        # 프로세서에서 처리가 완료된 프로세스 제거 및 프로세스 정보 설정
        self.tt = time - self.at
        self.ntt = round(self.tt / self.r_bt,2)
        self.wt = self.tt - self.r_bt                    # processor의 process

    def __str__(self):
        return "#Process" + str(self.id) + " AT = " + str(self.at) + " BT = " + str(self.r_bt) + " TT = " + str(self.tt) + " NTT = " + str(self.ntt) + " WT = " + str(self.wt)

# Processor Class Declair
class Processor:
    def __init__(self):
        self.running = False
        self.process = None

    # 프로세서에 프로세스 할당
    def ready_to_running(self,readyQue):
        if readyQue.isEmpty() != True:
            if self.running == False:
                self.process = readyQue.dequeue()
                self.running = True

    def running_process(self,time):
        if self.running == True:
            print("time" + str(time) + str(self.process)+ " " )
            self.process.bt -= 1
            # 프로세스 처리가 완료된 프로세스 상태 변경
            if self.process.bt == 0:
                self.running = False
                # process 정보 변경
                self.process.modify_process(time)
                self.process = None
                # 프로세스 종료되면
                return 1
        return 0 

# FCFS Scheduling Class 생성
class FCFS:
    # 생성자
    def __init__(self,input_value):
        self.process_ls=[]
        self.processor_ls=[]
        self.readyQueue = Nom_ReadyQueue()

        self.process_n = int(input_value[0])
        self.processor_n = int(input_value[1])
        self.bt_ls = list(input_value[2])
        self.at_ls = list(input_value[3])

        # 프로세스/프로세서 객체 생성
        for n in range(self.process_n):
            self.process_ls.append(Process(self.bt_ls[n],self.at_ls[n],n))
        for n in range(self.processor_n):
            self.processor_ls.append(Processor())
    
    # FCFS 멀티코어 프로세싱
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

# 공통 입력
def input_func():
    process_n = eval(input("#Process : "))
    processor_n = eval(input("#Processor : "))
    bt_ls = list(map(int,input("#Burst Time : ").split()))
    at_ls = list(map(int,input("#Arrive Time : ").split()))
    result = [process_n, processor_n, bt_ls, at_ls]
    return result

def main():
    FCFS(input_func()).mulitcore_processing()

# 메인 함수 호출
main()
