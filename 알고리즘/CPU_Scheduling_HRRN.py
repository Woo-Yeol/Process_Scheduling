import sys
import os
import time

# 프로세스 클래스
class process:
    def __init__(self,at,bt):
        self.at = at        # Arrival time
        self.bt = bt        # Burst time
        self.curr_time = 0  # 현재 처리 상태
        self.wait_time = 0  # 대기 시간
        self.ratio = 0      # response ratio

    def isComplete(self):   # 해당 프로세스 처리 완료 여부 조사
        if self.bt == self.curr_time: return True
        else: return False

# 프로세서 클래스
class processor:
    def __init__(self,n,processList):           # 생성자
        self.t = 0                              #  프로그램 수행시간(상대적)
        self.size = n                           # 프로세서 사이즈
        self.processList = processList          # 처리해야할 프로세스 리스트
        self.processor = [None] * self.size     # 현재 프로세서 상태 (None: 처리프로그램 없음, 프로세스: 해당 프로세스 처리중)
        self.queue = []                         # 처리 받기를 대기중인 프로세스 큐
        self.readied = []                       # 이미 쓰여진 프로세스 리스트
        self.chart = [[] for _ in range(self.size)]    # 출력될 간트차트


    def printState(self):                       # 프로세서 상태 출력
        os.system('cls')                        # 기존 출력 화면 지우기
        print("\n\t\t\t\t=======================================")
        print("\t\t\t\t            HRRN Scheduling            ")
        print("\t\t\t\t=======================================\n\n")
        # 프로세서들 출력
        for i in range(len(self.chart)):
            print("\t\t#Processor" + str(i+1) + ": ",end='')
            for ch in self.chart[i]:
                print(ch,end=' ')
            print("")
        # readyQueue 출력
        print("\n\t\t#ReadyQueue: ",end='')
        for q in self.queue:
            for idx in range(len(self.processList)):
                if q == self.processList[idx]:
                    print(chr(idx+65) + "(%.2f)"%(q.ratio),end=' ')
                    break
        print("\n")

    def isFirstEmpty(self):                     # 먼저 비어있는 프로세서를 반환 (없으면 -1)
        for i in range(self.size):
            if self.processor[i] == None:       # 처리 프로그램 없다면
                return i                        # 해당 프로세서 인덱스 반환
        return -1                               # 모든 프로세서가 프로세스를 처리중

    def readyQueue(self):                       # at에 도달한 프로세스를 처리하기 위해 queue에 삽입
        pl = len(self.processList)
        for i in range(pl):
            if self.processList[i].at == self.t:   # 현재 arrival time 이라면
                self.queue.append(self.processList[i])    # 큐로 삽입되어 할당받을 준비함
                self.readied.append(self.processList[i])

    def allocateProcess(self):                  # 큐의 response ratio 우선순위에 따라 프로세스 할당
        for i in range(len(self.queue)):        # 들어있는 큐만큼 반복
            idx = self.isFirstEmpty()           # 비어있는 프로세서 탐색
            if idx != -1:                       # 비어있는 프로세서가 있다면
                # response ratio가 가장 큰 프로세스
                # max 내장함수는 비용이 많이 들기에 직접 구현함
                max = self.queue[0].ratio
                index = 0
                for j in range(len(self.queue)):
                    if max < self.queue[j].ratio:
                        max = self.queue[j].ratio
                        index = j
                self.processor[idx] = self.queue.pop(index) # response ratio가 가장 큰 프로세스를 할당
            else: break                         # 비어있는 프로세스가 없으면 아무것도 실행하지 않음

    def chartIn(self):                          # 출력할 차트에 출력 내용을 넣어줌
        for i in range(len(self.processor)):
            state = True
            for idx in range(len(self.processList)):
                if self.processor[i] == self.processList[idx]:
                    self.chart[i].append(chr(idx+65))
                    state = False
                    break
            if state: self.chart[i].append("-")

    def calcResponseRatio(self,process):
        process.ratio = (process.bt + process.wait_time) / process.bt   # response ratio 계산


    def progressProcessor(self):
        self.readyQueue()                       # at에 도달한 프로세스를 처리하기 위해 queue에 삽입
        self.allocateProcess()                  # response ratio가 가장 큰 프로세스 할당
        self.chartIn()                          # 차트에 넣어줌
        for pro in self.processor:
            if pro != None:
                pro.curr_time += 1
        for q in self.queue:
            q.wait_time += 1                    # 큐의 프로세스들에 대해 대기시간 1증가
            self.calcResponseRatio(q)           # 큐에 들어있는 프로세스의 response ratio 계산
        self.t += 1
        self.printState()                       # 상태 출력
        time.sleep(1)
        for i in range(self.size):
            if self.processor[i] != None:
                if self.processor[i].isComplete():  # 해당 프로세스가 끝났다면
                    self.processor[i] = None        # 프로세스 종료

    def isOver(self):                           # 모든 프로세스 처리 여부 조사
        r = True
        p = True
        if len(self.readied) != len(self.processList):  # (1) 모든 프로세스가 readyQueue로 진입한다면
            r = False
        for pro in self.processor:                      # (2) 프로세서에서 처리하고 있는 프로세스 유무 검사 (모든 프로세서가 아무것도 처리하고 있지 않다면 True)
            if pro != None:
                p = False
                break
        if self.queue == [] and r and p:                # 큐가 비어있으며 (1),(2)를 만족한다면 True (모든 프로세스 처리 완료)
            return True
        else: return False

processList = []
print("Of Processes: ",end='')
process_n = int(sys.stdin.readline())               # 프로세스 개수
print("Of Processors: ",end='')
processor_n = int(sys.stdin.readline())             # 프로세서 개수
print("Arrival Time: ",end='')
AT = list(map(int,sys.stdin.readline().split()))    # Arrival Time 입력(프로세스 개수만큼)
print("Burst Time: ",end='')
BT = list(map(int,sys.stdin.readline().split()))    # Burst Time 입력(프로세스 개수만큼)
print("\n")

for i in range(process_n):
    processList.append(process(AT[i],BT[i]))        # 프로세스 객체에 AT와 BT를 넣고 processList에 추가
p = processor(processor_n,processList)              # 프로세서 객체 생성
while not p.isOver():
    p.progressProcessor()




