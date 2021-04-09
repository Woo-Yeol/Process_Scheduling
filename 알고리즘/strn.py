class PriorityQueue():
    def __init__(self): # 생성자
        self.items = []
    def isEmpty(self) : return len(self.items) == 0
    def size(self): return len(self.items)
    def clear(self): self.items = []
    def enqueue(self, item):    # 삽입 연산
        self.items.append(item)
    def findMaxIndex(self):             # 최대 우선순위 항목의 인덱스 반환
        if self.isEmpty(): return None
        else:
            highest = 0                 # 0번을 최대라고 하고
            for i in range(1, self.size()): # 모든 항목에 대해서
                if self.items[i].rt < self.items[highest].rt:   # rest Time이 가장 낮으면 가장 높은 우선순위
                    highest = i         # 인덱스 갱신
            return highest
    def dequeue(self):          # 삭제 연산
        highest = self.findMaxIndex()
        if highest is not None:
            return self.items.pop(highest)
    def peek(self):             # peek 연산
        highest = self.findMaxIndex()
        if highest is not None:
            return self.items[highest]

# Process Class Declair
class process:
    def __init__(self,bt,at,n):
        self.bt = int(bt)            # Process Burst Time
        self.at = int(at)            # Process Arrive Time
        self.rt = int(bt)            # rest time 잔여실행시간 
        self.tt =  0                 # Process Turnaround Time   반납시간 - At
        self.ntt = 0                 # Nomalized Turnaround Time TT/BT
        self.wt = 0                  # Waiting Time              TT-BT
        self.id = int(n+1)

    def __str__(self):
        return " #Process" + str(self.id) + " AT = " + str(self.at) + " BT = " + str(self.bt) + " RT = " + str(self.rt)  + " TT = " + str(self.tt) + " NTT = " + str(self.ntt) + " WT = " + str(self.wt)

# Processor Class Declair
class processor:
    def __init__(self):
        self.running = False
        self.process = None
        self.lock = False

# 현재시각에 priorityQueue로 구현한 readyQueue에 프로세스 저장하기
def readyQueue(time):
    for i in range(len(process_ls)):
        if (process_ls[i].at == time):
            readyQue.enqueue(process_ls[i])

# 프로세서에 프로세스 할당하기
def ready_to_running(i):
    if readyQue.isEmpty() != True:
        if processor_ls[i].running == False:
            processor_ls[i].process = readyQue.dequeue()
            processor_ls[i].running = True;

# 선점여부 확인하기
def check_rbt(time):
    checkQue= PriorityQueue()
    for i in range(len(process_ls)):                                            # cpu에 들어갈 후보 선출 (cpu안에 있는애들 + readyque에 있는애들)
        if process_ls[i].at <= time and process_ls[i].rt !=0:
            checkQue.enqueue(process_ls[i])

    for i in range(len(processor_ls)):                                           # 프로세서 수 만큼 순위 매기기
        to_go_process = checkQue.dequeue()                                             # to_go_process : cpu에 들어가야할 p
        for j in range(len(processor_ls)):
            if to_go_process == processor_ls[j].process:                                       # 우선순위(to_go_process)가 cpu안에 있으면
                processor_ls[j].lock = True
                break 
            elif to_go_process != processor_ls[j].process and processor_ls[j].lock==False:     # 우선순위가 cpu안에 없고, 마지막 cpu를 검사한 상태
                readyQue.enqueue(processor_ls[j].process)                        # 자리뺏긴 cpu안의 p는 다시 readyQue에 넣고
                processor_ls[j].process = readyQue.dequeue()                       # 해당 cpu는 ready큐에 있던 애랑 대체
                processor_ls[j].lock = True
                break

# 프로세서에서 프로세스 처리하기
def running_process(i,time):
    if processor_ls[i].running == True:
        print("time" + str(time) + str(processor_ls[i].process)+ " " )
        processor_ls[i].process.rt -= 1
        # 프로세스 처리가 완료된 프로세스 상태 변경
        if processor_ls[i].process.rt == 0:
                processor_ls[i].running = False
                # process 정보 변경
                modify_process(i,time)
                # 프로세스 종료되면
                return 1
    return 0              
# 프로세스 정보 수정하기
def modify_process(i,time):
    # 프로세서에서 처리가 완료된 프로세스 제거 및 프로세스 정보 설정
    processor_ls[i].process.tt = time - processor_ls[i].process.at
    processor_ls[i].process.ntt = round(processor_ls[i].process.tt / processor_ls[i].process.bt,2)
    processor_ls[i].process.wt = processor_ls[i].process.tt - processor_ls[i].process.bt                    # processor의 process
    processor_ls[i].process = None

# 메인 함수
def SRTN():
    # 프로세스/프로세서 리스트 생성
    global process_ls; process_ls = []
    global processor_ls; processor_ls=[]
    global readyQue; readyQue = PriorityQueue()

    # 입력
    process_n = eval(input("#Process : "))
    processor_n = eval(input("#Processor : "))
    bt_ls = list(map(int,input("#Burst Time : ").split()))
    at_ls = list(map(int,input("#Arrive Time : ").split()))
    
    # 프로세스/프로세서 객체 생성
    for n in range(process_n):
        process_ls.append(process(bt_ls[n],at_ls[n],n))
    for n in range(processor_n):
        processor_ls.append(processor())

    # 멀티코어 프로세스 스케쥴링
    time = 0; terminate = 0
    while(terminate != process_n):
        readyQueue(time)
        time += 1
    
        for i in range(len(processor_ls)):
            ready_to_running(i)                        # 큐에 프로세스가 있다면 비어있는 프로세서에 할당
            check_rbt(time)                            # 선점여부 확인하기
            terminate += running_process(i,time)       # 프로세서에 있는 프로세스의 Burst Time 1 빼기
              
    
    # 출력
    for i in range(len(process_ls)):
        print(str(process_ls[i]))

SRTN()