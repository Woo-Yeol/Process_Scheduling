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
                if self.items[i].bt < self.items[highest].bt:   # Burst Time이 가장 낮으면 가장 높은 우선순위
                    highest = i         # 인덱스 갱신
            return highest
    def dequeue(self):          # 삭제 연산
        highest = self.findMaxIndex()
        if highest is not None:
            return self.items.pop(highest)

    def nom_dequeue(self):              # 일반 큐에서 dequeue 연산
        if not self.isEmpty():
            return self.items.pop(0)

    def peek(self):             # peek 연산
        highest = self.findMaxIndex()
        if highest is not None:
            return self.items[highest]

class process:
    def __init__(self,at,bt,TQ):
        self.at = at        # Arrival time
        self.bt = bt        # Burst time
        self.curr_time = bt  # 현재 처리 상태
        self.wait_time = 0  # 대기 시간
        self.tt = 0
        self.ntt = 0
        self.ratio = 0      # response ratio
        self.time_limit = TQ
        self.left_time = TQ

    def isComplete(self):   # 해당 프로세스 처리 완료 여부 조사
        # if self.bt == self.curr_time: return True
        if self.curr_time == 0 : return True
        else: return False

    def isTimeover(self):
        if self.left_time == 0 :
            self.left_time = self.time_limit
            return True
        else:
            return False

class processor:
    def __init__(self,n,processList, TQ):           # 생성자
        self.t = 0                              #  프로그램 수행시간(상대적)
        self.size = n                           # 프로세서 사이즈
        self.processList = processList          # 처리해야할 프로세스 리스트
        self.processor = [None] * self.size     # 현재 프로세서 상태 (None: 처리프로그램 없음, 프로세스: 해당 프로세스 처리중)
        self.queue = PriorityQueue()            # 처리 받기를 대기중인 프로세스 큐
        self.readied = []                       # 이미 쓰여진 프로세스 리스트
        self.chart = [[] for _ in range(self.size)]    # 출력될 간트차트
        self.done_process = [None] * len(processList)
        self.time_limit = TQ

    def isFirstEmpty(self):                     # 먼저 비어있는 프로세서를 반환 (없으면 -1)
        for i in range(self.size):
            if self.processor[i] == None:       # 처리 프로그램 없다면
                return i                        # 해당 프로세서 인덱스 반환
        return -1                               # 모든 프로세서가 프로세스를 처리중

    def readyQueue(self):
        pl = len(self.processList)
        for i in range(pl):
            if self.processList[i].at == self.t:
                self.queue.enqueue(self.processList[i])      # 현재 arrival time이라면
                self.readied.append(self.processList[i])    # 큐로 삽입되어 할당받을 준비

    def allocateProcess_FCFS(self):
        for _ in range(self.queue.size()):
            idx = self.isFirstEmpty()
            if idx != -1:
                self.processor[idx] = self.queue.nom_dequeue()
            else : break

    def progressProcessor(self):
        self.readyQueue()
        self.allocateProcess_FCFS()

        for pro in self.processor:
            if pro != None:
                pro.curr_time -= 1
                pro.left_time -= 1
        
        
            # self.printState()

        for i in range(self.size):
            if self.processor[i] != None:
                if self.processor[i].isComplete():
                    self.processor[i].tt = self.t - self.processor[i].at + 1
                    self.processor[i].wait_time = self.processor[i].tt - self.processor[i].bt
                    self.processor[i].ntt = self.processor[i].tt / self.processor[i].bt
                    # self.processor[i].curr_time = 0
                    self.processor[i] = None

        for i in range(self.size):
            if self.processor[i] != None:
                if self.processor[i].isTimeover():
                    self.queue.enqueue(self.processor[i])
                    self.processor[i] = None
                    
        self.t += 1


    def isOver(self):
        r = True
        p = True
        if len(self.readied) != len(self.processList):
            r = False

        for pro in self.processor:
            if pro != None:
                p = False
                break
        if self.queue.isEmpty() and r and p:
            return True
        else : return False


def INPUT():
    n_process = eval(input("# of Processes : "))
    n_processor = eval(input("# of Processors : "))
    AT = list(map(int, input("Arrival time : ").split()))
    BT = list(map(int, input("Burst time : ").split()))
    TQ = eval(input("Time quantum for RR : "))

    return n_process, n_processor, list(AT), list(BT), TQ



process_n, processor_n, AT, BT, TQ = INPUT()
processList = []

for i in range(process_n):
    processList.append(process(AT[i], BT[i], TQ))
p = processor(processor_n, processList, TQ)
while not p.isOver():
    p.progressProcessor()

print(p)


