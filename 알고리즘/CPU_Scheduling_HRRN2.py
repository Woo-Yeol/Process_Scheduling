import sys
import os
import time


# Python list를 이용한 PriorityQueue ADT 구현.
class ReadyQueue:
    # 생성자
    def __init__(self):
        self.items = []

    # 비어있는지 확인
    def isEmpty(self):
        return len(self.items) == 0

    # 큐의 크기 확인
    def size(self):
        return len(self.items)

    # 큐 초기화
    def clear(self):
        self.items = []

    # 큐 삽입
    def enqueue(self, item):  # 삽입 연산
        self.items.append(item)

    # 최대 우선순위 항목의 인덱스 반환
    def findMaxIndex(self):
        if self.isEmpty():
            return None
        else:
            highest = 0  # 0번을 최대라고 하고
            for i in range(1, self.size()):  # 모든 항목에 대해서
                if self.items[i].ratio > self.items[highest].ratio:  # response ratio가 높으면 우선순위
                    highest = i  # 인덱스 갱신
            return highest

    # 큐 삭제 연산
    def dequeue(self):
        highest = self.findMaxIndex()
        if highest is not None:
            return self.items.pop(highest)

    # peek 연산
    def peek(self):
        highest = self.findMaxIndex()
        if highest is not None:
            return self.items[highest]

    # 레디 큐 생성 연산
    def readyQueue(self, process, time):
        for pro in process:
            if (pro.at == time):
                self.enqueue(pro)

# 프로세스 클래스
class Process:
    def __init__(self,at,bt,n):
        self.at = at        # Arrival time
        self.bt = bt        # Burst time
        self.rbt = bt       # Burst time 기억
        self.tt = 0
        self.ntt = 0
        self.wt = 0         # 대기 시간
        self.ratio = 0      # response ratio
        self.id = n+1

    def meditate(self,time):
        self.tt = time - self.at
        self.ntt = round(self.tt / self.rbt, 2)
        self.wt = self.tt - self.rbt
        self.ratio = (self.rbt + self.wt) / self.rbt

    def __str__(self):
        return "#Process" + str(self.id) + " AT = " + str(self.at) + " BT = " + str(self.bt) + " TT = " + str(
            self.tt) + " NTT = " + str(self.ntt) + " WT = " + str(self.wt)

# 프로세서 클래스
class Processor:
    def __init__(self):           # 생성자
        self.running = False
        self.process = None


    def allocateProcess(self,queue):
        if queue.isEmpty() != True:
            if self.running == False:
                self.process = queue.dequeue()
                self.running = True

    def progressProcessor(self,time):
        if self.running == True:
            self.process.bt -= 1
            return self.BurnOut(time)
        return 0

    def BurnOut(self,time):
        if self.process.bt == 0:
            self.running = False
            self.process.meditate(time)
            self.process = None
            return 1
        return 0

class HRRN:
    def __init__(self,input):
        self.process_n = input[0]
        self.processor_n = input[1]
        self.process = []
        self.processor = []
        self.at = input[2]
        self.bt = input[3]
        self.queue = ReadyQueue()
        self.chart = [[] for _ in range(self.processor_n)]

        # 프로세스/프로세서 객체 생성
        for i in range(self.process_n):
            self.process.append(Process(self.at[i],self.bt[i],i))
        for i in range(self.processor_n):
            self.processor.append(Processor())


    # HRRN 멀티코어 프로세싱
    def multicore_processing(self):
        time = 0
        terminate = 0
        while terminate != self.process_n:
            self.queue.readyQueue(self.process,time)
            time += 1
            for proc in self.processor:
                proc.allocateProcess(self.queue)
                terminate += proc.progressProcessor(time)
            # 출력
            for process in self.process:
                print(str(process))


def input_func():
    print("Of Processes: ", end='')
    process_n = int(sys.stdin.readline())  # 프로세스 개수
    print("Of Processors: ", end='')
    processor_n = int(sys.stdin.readline())  # 프로세서 개수
    print("Arrival Time: ", end='')
    AT = list(map(int, sys.stdin.readline().split()))  # Arrival Time 입력(프로세스 개수만큼)
    print("Burst Time: ", end='')
    BT = list(map(int, sys.stdin.readline().split()))  # Burst Time 입력(프로세스 개수만큼)
    print("\n")
    return [process_n,processor_n,AT,BT]


def main():
    HRRN(input_func()).multicore_processing()

main()