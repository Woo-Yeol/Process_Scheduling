# Python list를 이용한 PriorityQueue ADT 구현.
class ReadyQueue:
    # 생성자
    def __init__(self):
        self.items = []

    # 비어있는지 확인
    def isEmpty(self): return len(self.items) == 0

    # 큐의 크기 확인
    def size(self): return len(self.items)

    # 큐 초기화
    def clear(self): self.items = []

    # 큐 삽입
    def enqueue(self, item):  self.items.append(item)

    # 큐 삭제 연산
    def dequeue(self):
        if not self.isEmpty(): return self.items.pop(0)

    # peek 연산
    def peek(self):
        if not self.isEmpty(): return self.items[0]

    # 레디 큐 생성 연산
    def readyQue(self, process_ls, time):
        for process in process_ls:
            if (process.at == time): self.enqueue(process)


class PriorityReadyQueue(ReadyQueue):

    def dequeue(self):
        highest = self.findMaxIndex()
        if highest is not None:
            return self.items.pop(highest)
    # peek 연산
    def peek(self):
        highest = self.findMaxIndex()
        if highest is not None:
            return self.items[highest]


class SPNPriorityReadyQueue(PriorityReadyQueue):
    def findMaxIndex(self):
        if self.isEmpty(): return None
        else:
            highest = 0  # 0번을 최대라고 하고
            for i in range(1, self.size()):  # 모든 항목에 대해서
                if self.items[i].bt < self.items[highest].bt:  # Burst Time이 가장 낮으면 가장 높은 우선순위
                    highest = i  # 인덱스 갱신
            return highest


class SRTNPriorityReadyQueue(PriorityReadyQueue):
    def findMaxIndex(self):  # 최대 우선순위 항목의 인덱스 반환
        if self.isEmpty(): return None
        else:
            highest = 0  # 0번을 최대라고 하고
            for i in range(1, self.size()):  # 모든 항목에 대해서
                if self.items[i].bt < self.items[highest].bt:  # rest Time이 가장 낮으면 가장 높은 우선순위
                    highest = i  # 인덱스 갱신
                elif self.items[i].bt == self.items[highest].bt:  # 만약 resetTime이 같으면 먼저 온게 가장 높은 우선순위
                    highest = self.items[i].at if self.items[i].at < self.items[highest].at else self.items[highest].at
            return highest


class HRRNPriorityReadyQueue(PriorityReadyQueue):
    def findMaxIndex(self):
        if self.isEmpty(): return None
        else:
            highest = 0  # 0번을 최대라고 하고
            for i in range(1, self.size()):  # 모든 항목에 대해서
                if self.items[i].ratio > self.items[highest].ratio:  # response ratio가 높으면 우선순위
                    highest = i  # 인덱스 갱신
            return highest


# Process Class Declair
class Process:
    def __init__(self, bt, at, n,tq=0):
        self.bt = int(bt)  # Process Burst Time
        self.rbt = int(bt)  # Process Burst Time 기억용
        self.at = int(at)  # Process Arrive Time
        self.tt = 0  # Process Turnaround Time   반납시간 - At
        self.ntt = 0  # Nomalized Turnaround Time TT/BT
        self.wt = 0  # Waiting Time              TT-BT
        self.id = int(n + 1)
        self.tq = int(tq)  # Process Time Quantum
        self.r_tq = int(tq)  # Process Time Quantum 기억용
        self.ratio = 0

    def modify_process(self, time):
        # 프로세서에서 처리가 완료된 프로세스 제거 및 프로세스 정보 설정
        self.tt = time - self.at
        self.ntt = round(self.tt / self.rbt, 2)
        self.wt = self.tt - self.rbt  # processor의 process

    def __str__(self):
        return "#Process" + str(self.id) + " AT = " + str(self.at) + " BT = " + str(self.bt) + " TT = " + str(
            self.tt) + " NTT = " + str(self.ntt) + " WT = " + str(self.wt)

    def calc_ratio(self):
        self.ratio = (self.rbt + self.wt) / self.rbt


# Processor Class Declair
class Processor:
    def __init__(self):
        self.running = False
        self.process = None
        self.lock = False

    # 프로세서에 프로세스 할당
    def ready_to_running(self, readyQue):
        for pro in readyQue.items:
            pro.calc_ratio()
        if readyQue.isEmpty() != True:
            if self.running == False:
                self.process = readyQue.dequeue()
                self.running = True

    def running_process(self, time):
        if self.running == True:
            self.process.bt -= 1
            print("time" + str(time) + str(self.process) + " ")
            # 프로세스 처리가 완료된 프로세스 상태 변경
            if self.process.bt == 0:
                self.running = False
                # process 정보 변경
                self.process.modify_process(time)
                self.process = None
                # 프로세스 종료되면
                return 1
        return 0

    def time_progress(self, readyQue):
        if self.running == True:
            self.process.tq -= 1
            if self.process.tq == 0:  # 자원 제한시간이 지나면
                self.running = False  # 자원 반납
                self.process.tq = self.process.r_tq  # 해당 프로세스의 다음 처리를 위해 제한시간 다시 부여
                readyQue.enqueue(self.process)  # 자원을 반납한 프로세스는 큐의 맨 뒤에서 다시 대기
                self.process = None  # 자원 반납 후 할당 해제


class Scheduling:
    def __init__(self, input_value):
        self.process_ls = []
        self.processor_ls = []
        self.process_n = int(input_value[0])
        self.processor_n = int(input_value[1])
        self.bt_ls = list(input_value[2])
        self.at_ls = list(input_value[3])
        self.scheduling = input_value[4]
        if self.scheduling == 'FCFS': self.readyQueue = ReadyQueue()
        if self.scheduling == 'RR':
            self.readyQueue = ReadyQueue()
            self.time_quantum = eval(input("#Time Quantum : "))
        if self.scheduling == 'SPN': self.readyQueue = SPNPriorityReadyQueue()
        if self.scheduling == 'SRTN': self.readyQueue = SRTNPriorityReadyQueue()
        if self.scheduling == 'HRRN': self.readyQueue = HRRNPriorityReadyQueue()
        # if self.scheduling == 'DTRR': self.readyQueue = DTRRPriorityReadyQueue()

        # 프로세스/프로세서 객체 생성
        for n in range(self.process_n):
            if self.scheduling == 'RR':
                self.process_ls.append(Process(self.bt_ls[n], self.at_ls[n], n, self.time_quantum))
            else:
                self.process_ls.append(Process(self.bt_ls[n], self.at_ls[n], n))
        for n in range(self.processor_n):
            self.processor_ls.append(Processor())

    def mulitcore_processing(self):
        time = 0;
        terminate = 0
        while terminate != self.process_n:
            self.readyQueue.readyQue(self.process_ls, time)
            if self.scheduling == 'RR':
                for processor in self.processor_ls:
                    processor.time_progress(self.readyQueue)
                    # 시간 경과에 따른 제한시간(Time Quantum)처리
            time += 1
            for processor in self.processor_ls:
                # 큐에 프로세스가 있다면 비어있는 프로세서에 할당
                processor.ready_to_running(self.readyQueue)
                if self.scheduling == 'SRTN':
                    if self.is_cpu_full(time) == True and self.readyQueue.isEmpty() != True:
                        self.check_rbt(time)  # 선점여부 확인하기
                # 프로세서에 있는 프로세스 처리하기
                terminate += processor.running_process(time)
        # 출력
        for process in self.process_ls:
            print(str(process))

    # CPU가 다 꽉찼는지 여부 확인
    def is_cpu_full(self,time):
        cnt = 0
        for processor in self.processor_ls:
            if processor.running == True: cnt += 1
        if cnt == len(self.processor_ls): return True
        else: return False

    # 선점여부 확인하기
    def check_rbt(self,time):
        for i in range(len(self.process_ls)):  # cpu에 들어갈 후보 선출 (cpu안에 있는애들 + readyque에 있는애들)
            if self.process_ls[i].at <= time and self.process_ls[i].bt != 0:
                self.readyQueue.enqueue(self.process_ls[i])

        for i in range(len(self.processor_ls)):  # 프로세서 수 만큼 순위 매기기
            to_go_process = self.readyQueue.dequeue()  # to_go_process : cpu에 들어가야할 p
            for j in range(len(self.processor_ls)):
                if to_go_process == self.processor_ls[j].process:  # 우선순위(to_go_process)가 cpu안에 있으면
                    self.processor_ls[j].lock = True
                    break
                elif to_go_process != self.processor_ls[j].process and self.processor_ls[
                    j].lock == False:  # 우선순위가 cpu안에 없고, 안잠겨있으면
                    self.readyQueue.enqueue(self.processor_ls[j].process)  # 자리뺏긴 cpu안의 p는 다시 readyQue에 넣고
                    self.processor_ls[j].process = self.readyQueue.dequeue()  # 해당 cpu는 ready큐에 있던 애랑 대체
                    self.processor_ls[j].lock = True
                    break
        for j in range(len(self.processor_ls)):
            self.processor_ls[j].lock = False

def input_func():
    schedulingDict = {1: 'FCFS', 2: 'RR', 3: 'SPN', 4: 'SRTN', 5: 'HRRN', 6: 'DTRR'}
    print("\n1.FCFS  2.RR  3.SPN  4.SRTN  5.HRRN  6.DTRR")
    scheduling = int(input("#Select Scheduling: "))
    process_n = eval(input("#Process : "))
    processor_n = eval(input("#Processor : "))
    bt_ls = list(map(int, input("#Burst Time : ").split()))
    at_ls = list(map(int, input("#Arrive Time : ").split()))
    result = [process_n, processor_n, bt_ls, at_ls,schedulingDict[scheduling]]
    return result


def main():
    Scheduling(input_func()).mulitcore_processing()

# 메인 함수 호출
main()