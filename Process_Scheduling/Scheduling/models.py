from django.db import models

# 랜덤한 우선순위를 설정하기 위한 random import
import random

# 우선순위를 선정하기 위한 변수
HIGH = 1
MEDIUM = 2
LOW = 3
priority = [HIGH, MEDIUM, LOW]


# Python list를 이용한 Queue ADT 구현.
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
    def enqueue(self, item):
        self.items.append(item)

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


# Python list를 이용하여 ReadyQueue를 상속받아 PriorityQueue ADT 구현
class PriorityReadyQueue(ReadyQueue):
    # dequeue 연산 오버라이딩
    def dequeue(self):
        highest = self.findMaxIndex()
        if highest is not None:
            return self.items.pop(highest)

    # peek 연산 오버라이딩
    def peek(self):
        highest = self.findMaxIndex()
        if highest is not None:
            return self.items[highest]


# Python list를 이용하여 PriorityQueue 상속받아 SPN 알고리즘의 구현을 위한 SPNPriorityQueue ADT 구현
class SPNPriorityReadyQueue(PriorityReadyQueue):
    # 우선순위를 검색하는 findmaxIndex 오버라이딩
    def findMaxIndex(self):
        if self.isEmpty():
            return None
        else:
            highest = 0  # 0번을 최대라고 하고
            for i in range(1, self.size()):  # 모든 항목에 대해서
                if self.items[i].bt < self.items[highest].bt:  # Burst Time이 가장 낮으면 가장 높은 우선순위
                    highest = i  # 인덱스 갱신
            return highest


# Python list를 이용하여 PriorityReadyQueue 상속받아 SRTN 알고리즘의 구현을 위한 SRTNPriorityQueue ADT 구현
class SRTNPriorityReadyQueue(PriorityReadyQueue):
    # 우선순위를 검색하는 findmaxIndex 오버라이딩
    def findMaxIndex(self):  # 최대 우선순위 항목의 인덱스 반환
        if self.isEmpty():
            return None
        else:
            highest = 0  # 0번을 최대라고 하고
            for i in range(1, self.size()):  # 모든 항목에 대해서
                if self.items[i].bt < self.items[highest].bt:  # rest Time이 가장 낮으면 가장 높은 우선순위
                    highest = i  # 인덱스 갱신
                elif self.items[i].bt == self.items[highest].bt:  # 만약 resetTime이 같으면 먼저 온게 가장 높은 우선순위
                    if self.items[i].at < self.items[highest].at: highest = i
            return highest


# Python list를 이용하여 PriorityReadyQueue 상속받아 HRRN 알고리즘의 구현을 위한 HRRNPriorityQueue ADT 구현
class HRRNPriorityReadyQueue(PriorityReadyQueue):
    # 우선순위를 검색하는 findmaxIndex 오버라이딩
    def findMaxIndex(self):
        if self.isEmpty():
            return None
        else:
            highest = 0  # 0번을 최대라고 하고
            for i in range(1, self.size()):  # 모든 항목에 대해서
                if self.items[i].ratio > self.items[highest].ratio:  # response ratio가 높으면 우선순위
                    highest = i  # 인덱스 갱신
            return highest


# Python list를 이용하여 ReadyQueue 상속받아 DTRR 알고리즘의 구현을 위한 DTRRPriorityQueue 구현
class DTRRReadyQueue(ReadyQueue):
    def __init__(self):
        self.items = []
        self.save_bt = 0
        self.save_n = 0
        self.d_tq = 0

    def readyQue(self, process_ls, time):  # 부모클래스 메소드 overriding
        for process in process_ls:
            if process.at == time:
                self.enqueue(process)
                self.get_DTQ()  # 새로운 process가 삽입될때마다 get DTQ

    def get_DTQ(self):
        for process in self.items:
            if process.is_new == True:  # 큐에 처음 들어온 process에 대해
                self.save_bt += process.bt
                self.save_n += 1

        self.d_tq = round(self.save_bt / self.save_n)  # 누적 평균 계산


# Process Class 선언
class Process:
    # 프로세스의 속성을 정의
    def __init__(self, bt, at, n, tq=0):
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
        self.is_new = True
        # DTRR 알고리즘을 위한 우선순위 속성을 랜덤하게 확인한다.
        self.priority = random.choice(priority)

    # 프로세스 정보 설정
    def modify_process(self, time):
        self.tt = time - self.at
        self.ntt = round(self.tt / self.rbt, 2)
        self.wt = self.tt - self.rbt  # processor의 process

    # HRRN 알고리즘을 위한 ratio 계산식
    def calc_ratio(self):
        self.ratio = (self.rbt + self.wt) / self.rbt

    def __str__(self):
        return "#Process" + str(self.id) + " AT = " + str(self.at) + " BT = " + str(self.bt) + " TT = " + str(
            self.tt) + " NTT = " + str(self.ntt) + " WT = " + str(self.wt)


# Processor Class 선언
class Processor:
    # 프로세서의 속성을 정의
    def __init__(self):
        self.running = False
        self.process = None
        self.lock = False
        self.processor_memory = []

    # 프로세서에 프로세스 할당
    def ready_to_running(self, readyQue):
        if readyQue.isEmpty() != True:
            if self.running == False:
                self.process = readyQue.dequeue()
                self.running = True

    # 프로세스를 실행한다 -> Burst Time을 1초 감소시킨다.
    def running_process(self, time):
        # 프로세서에 어떤 프로세스가 실행되었는지 기록한다. -> 간트차트의 구현을 위한 정보 기록
        if self.process == None:
            self.processor_memory.append(None)
        else:
            self.processor_memory.append(self.process.id)

        # 실행중인 프로세스의 Burst Time을 1초 감소시킨다.
        if self.running == True:
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

    def HRRNrunning_process(self, time):
        # 프로세서에 어떤 프로세스가 실행되었는지 기록한다. -> 간트차트의 구현을 위한 정보 기록
        # running_process와는 다르게 modify_process가 없음
        if self.process == None:
            self.processor_memory.append(None)
        else:
            self.processor_memory.append(self.process.id)

        # 실행중인 프로세스의 Burst Time을 1초 감소시킨다.
        if self.running == True:
            self.process.bt -= 1
            # 프로세스 처리가 완료된 프로세스 상태 변경
            if self.process.bt == 0:
                self.running = False
                # process 정보 변경
                self.process = None
                # 프로세스 종료되면
                return 1
        return 0

    # RR 알고리즘 구현을 위한 프로세스 진행 시간을 확인하고 자원을 회수한다.
    def time_progress(self, readyQue):
        if self.running == True:
            self.process.tq -= 1
            if self.process.tq == 0:  # 자원 제한시간이 지나면
                self.running = False  # 자원 반납
                self.process.tq = self.process.r_tq  # 해당 프로세스의 다음 처리를 위해 제한시간 다시 부여
                readyQue.enqueue(self.process)  # 자원을 반납한 프로세스는 큐의 맨 뒤에서 다시 대기
                self.process = None  # 자원 반납 후 할당 해제

    # DTRR 알고리즘의 가장 낮은 우선순위의 프로세스의 진행시간을 확인하고 자원을 회수한다.
    def time_progress_Lpriority(self, readyQue):
        if self.running == True:
            self.process.tq += 1

            if self.process.tq >= (readyQue.d_tq - 0.15 * readyQue.d_tq):  # LOW priority프로세스에 대해 tq -15%
                self.running = False  # 자원 반납
                self.process.tq = 0  # 해당 프로세스의 다음 처리를 위해 제한시간 다시 부여
                self.process.is_new = False
                readyQue.enqueue(self.process)  # 자원을 반납한 프로세스는 큐의 맨 뒤에서 다시 대기
                self.process = None  # 자원 반납 후 할당 해제

    # DTRR 알고리즘의 중간 순위의 프로세스의 진행시간을 확인하고 자원을 회수한다.
    def time_progress_Mpriority(self, readyQue):
        if self.running == True:
            self.process.tq += 1

            if self.process.tq >= (readyQue.d_tq + 0 * readyQue.d_tq):  # 자원 제한시간이 지나면
                self.running = False  # 자원 반납
                self.process.tq = 0  # 해당 프로세스의 다음 처리를 위해 제한시간 다시 부여
                self.process.is_new = False
                readyQue.enqueue(self.process)  # 자원을 반납한 프로세스는 큐의 맨 뒤에서 다시 대기
                self.process = None  # 자원 반납 후 할당 해제

    # DTRR 알고리즘의 중간 순위의 프로세스의 진행시간을 확인하고 자원을 회수한다.
    def time_progress_Hpriority(self, readyQue):
        if self.running == True:
            self.process.tq += 1

            if self.process.tq >= (readyQue.d_tq + 0.15 * readyQue.d_tq):  # HIGH priority프로세스에 대해 tq + 15%
                self.running = False  # 자원 반납
                self.process.tq = 0  # 해당 프로세스의 다음 처리를 위해 제한시간 다시 부여
                self.process.is_new = False
                readyQue.enqueue(self.process)  # 자원을 반납한 프로세스는 큐의 맨 뒤에서 다시 대기
                self.process = None  # 자원 반납 후 할당 해제


# FCFS Scheduling Class 생성
class FCFS:
    # 생성자
    def __init__(self, input_value):
        self.process_ls = []
        self.processor_ls = []
        self.readyQueue = ReadyQueue()

        self.process_n = int(input_value[0])
        self.processor_n = int(input_value[1])
        self.bt_ls = list(input_value[2])
        self.at_ls = list(input_value[3])

        # 프로세스/프로세서 객체 생성
        for n in range(self.process_n):
            self.process_ls.append(Process(self.bt_ls[n], self.at_ls[n], n))
        for n in range(self.processor_n):
            self.processor_ls.append(Processor())

    # FCFS 멀티코어 프로세싱
    def multicore_processing(self):
        time = 0;
        terminate = 0
        while (terminate != self.process_n):
            self.readyQueue.readyQue(self.process_ls, time)
            time += 1
            for processor in self.processor_ls:
                # 큐에 프로세스가 있다면 비어있는 프로세서에 할당
                processor.ready_to_running(self.readyQueue)
                # 프로세서에 있는 프로세스 처리하기
                terminate += processor.running_process(time)
        # 출력
        result = []
        for process in self.process_ls:
            result.append(
                [process.at, process.rbt, process.wt, process.tt, process.ntt])  # 실행이 종료된 프로세스의 속성을 값을 저장한 리스트
        p_memory = []
        for processor in self.processor_ls:
            p_memory.append(processor.processor_memory)  # 프로세서의 로그가 저장된 리스트
        return (result, p_memory)

    # RR Scheduling Class 생성


class RR:
    # 생성자
    def __init__(self, input_value, time_quantum):
        self.process_ls = []
        self.processor_ls = []
        self.readyQueue = ReadyQueue()

        self.process_n = int(input_value[0])
        self.processor_n = int(input_value[1])
        self.bt_ls = list(input_value[2])
        self.at_ls = list(input_value[3])
        self.time_quantum = eval(time_quantum)

        # 프로세스/프로세서 객체 생성
        for n in range(self.process_n):
            self.process_ls.append(Process(self.bt_ls[n], self.at_ls[n], n, self.time_quantum))
        for n in range(self.processor_n):
            self.processor_ls.append(Processor())

    # RR 멀티코어 프로세싱
    def multicore_processing(self):
        time = 0;
        terminate = 0
        while (terminate != self.process_n):
            self.readyQueue.readyQue(self.process_ls, time)
            for processor in self.processor_ls:
                processor.time_progress(self.readyQueue)
                # 시간 경과에 따른 제한시간(Time Quantum)처리
            time += 1
            for processor in self.processor_ls:
                # 큐에 프로세스가 있다면 비어있는 프로세서에 할당
                processor.ready_to_running(self.readyQueue)
                # 프로세서에 있는 프로세스 처리하기
                terminate += processor.running_process(time)

        # 출력
        result = []
        for process in self.process_ls:
            result.append(
                [process.at, process.rbt, process.wt, process.tt, process.ntt])  # 실행이 종료된 프로세스의 속성을 값을 저장한 리스트
        p_memory = []
        for processor in self.processor_ls:
            p_memory.append(processor.processor_memory)  # 프로세서의 로그가 저장된 리스트
        return (result, p_memory)

    # SPN Scheduling Class 생성


class SPN:
    # 생성자
    def __init__(self, input_value):
        self.process_ls = []
        self.processor_ls = []
        self.readyQueue = SPNPriorityReadyQueue()

        self.process_n = int(input_value[0])
        self.processor_n = int(input_value[1])
        self.bt_ls = list(input_value[2])
        self.at_ls = list(input_value[3])

        # 프로세스/프로세서 객체 생성
        for n in range(self.process_n):
            self.process_ls.append(Process(self.bt_ls[n], self.at_ls[n], n))
        for n in range(self.processor_n):
            self.processor_ls.append(Processor())

    # SPN 멀티코어 프로세싱
    def multicore_processing(self):
        time = 0;
        terminate = 0
        while (terminate != self.process_n):
            self.readyQueue.readyQue(self.process_ls, time)
            time += 1
            for processor in self.processor_ls:
                # 큐에 프로세스가 있다면 비어있는 프로세서에 할당
                processor.ready_to_running(self.readyQueue)
                # 프로세서에 있는 프로세스 처리하기
                terminate += processor.running_process(time)
        # 출력
        result = []
        for process in self.process_ls:
            result.append(
                [process.at, process.rbt, process.wt, process.tt, process.ntt])  # 실행이 종료된 프로세스의 속성을 값을 저장한 리스트
        p_memory = []
        for processor in self.processor_ls:
            p_memory.append(processor.processor_memory)  # 프로세서의 로그가 저장된 리스트
        return (result, p_memory)

    # SRTN Scheduling Class 생성


class SRTN:
    # 생성자
    def __init__(self, input_value):
        self.process_ls = []
        self.processor_ls = []
        self.readyQueue = SRTNPriorityReadyQueue()
        self.process_n = int(input_value[0])
        self.processor_n = int(input_value[1])
        self.bt_ls = list(input_value[2])
        self.at_ls = list(input_value[3])

        # 프로세스/프로세서 객체 생성
        for n in range(self.process_n):
            self.process_ls.append(Process(self.bt_ls[n], self.at_ls[n], n))
        for n in range(self.processor_n):
            self.processor_ls.append(Processor())

    # CPU가 다 꽉찼는지 여부 확인
    def is_cpu_full(self, time):
        cnt = 0
        for i in range(len(self.processor_ls)):
            if self.processor_ls[i].running == True:
                cnt += 1
        if cnt == len(self.processor_ls):
            return True
        else:
            return False

    # 모든 프로세스의 RT를 확인하여 실행해야할 프로세스의 리스트를 만들고 이를 통해 확인된 프로세스를 자원 회수의 횟수가 가장 적은 방향으로 교환을 진행한다.
    def check_rbt(self, time):
        checkQue = SRTNPriorityReadyQueue()
        for i in range(len(self.process_ls)):  # cpu에 들어갈 후보 선출 (cpu안에 있는애들 + readyque에 있는애들)
            if self.process_ls[i].at <= time and self.process_ls[i].bt != 0:
                checkQue.enqueue(self.process_ls[i])

        for i in range(len(self.processor_ls)):  # 프로세서 수 만큼 순위 매기기
            to_go_process = checkQue.dequeue()  # to_go_process : cpu에 들어가야할 p
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

    # SRTN 멀티코어 프로세싱
    def multicore_processing(self):
        time = 0;
        terminate = 0
        while (terminate != self.process_n):
            self.readyQueue.readyQue(self.process_ls, time)
            time += 1
            for processor in self.processor_ls:
                # 큐에 프로세스가 있다면 비어있는 프로세서에 할당
                processor.ready_to_running(self.readyQueue)
                if self.is_cpu_full(time) == True and self.readyQueue.isEmpty() != True:
                    self.check_rbt(time)
                # 프로세서에 있는 프로세스 처리하기
                terminate += processor.running_process(time)
        # 출력
        result = []
        for process in self.process_ls:
            result.append(
                [process.at, process.rbt, process.wt, process.tt, process.ntt])  # 실행이 종료된 프로세스의 속성을 값을 저장한 리스트
        p_memory = []
        for processor in self.processor_ls:
            p_memory.append(processor.processor_memory)  # 프로세서의 로그가 저장된 리스트
        return (result, p_memory)

    # HRRN Scheduling Class 생성
class HRRN:
    def __init__(self, input_value):
        self.process_ls = []
        self.processor_ls = []
        self.readyQueue = HRRNPriorityReadyQueue()

        self.process_n = int(input_value[0])
        self.processor_n = int(input_value[1])
        self.bt_ls = list(input_value[2])
        self.at_ls = list(input_value[3])

        # 프로세스/프로세서 객체 생성
        for n in range(self.process_n):
            self.process_ls.append(Process(self.bt_ls[n], self.at_ls[n], n))
        for n in range(self.processor_n):
            self.processor_ls.append(Processor())

    def multicore_processing(self):
        time = 0;
        terminate = 0
        while terminate != self.process_n:
            for process in self.process_ls:
                process.calc_ratio()
            self.readyQueue.readyQue(self.process_ls, time)
            time += 1
            for processor in self.processor_ls:
                # 큐에 프로세스가 있다면 비어있는 프로세서에 할당
                processor.ready_to_running(self.readyQueue)
                # 프로세서에 있는 프로세스 처리하기
                terminate += processor.HRRNrunning_process(time)
            for process in self.readyQueue.items:   
            # 프로세서에 들어가지 못한 프로세스 들에 대해 wt 증가
                if process.at < time and process.bt != 0:
                    process.wt += 1
                    
        for process in self.process_ls:
        # tt 및 ntt 계산
            process.tt = process.rbt + process.wt
            process.ntt = round(process.tt / process.rbt, 2)
            
        # 출력
        result = []
        for process in self.process_ls:
            result.append(
                [process.at, process.rbt, process.wt, process.tt, process.ntt])  # 실행이 종료된 프로세스의 속성을 값을 저장한 리스트
        p_memory = []
        for processor in self.processor_ls:
            p_memory.append(processor.processor_memory)  # 프로세서의 로그가 저장된 리스트
        return (result, p_memory)

    # DTRR Scheduling Class 생성


class DTRR:
    # 생성자
    def __init__(self, input_value):
        self.process_ls = []
        self.processor_ls = []
        self.readyQueue = DTRRReadyQueue()

        self.process_n = int(input_value[0])
        self.processor_n = int(input_value[1])
        self.bt_ls = list(input_value[2])
        self.at_ls = list(input_value[3])

        # 프로세스/프로세서 객체 생성
        for n in range(self.process_n):
            self.process_ls.append(Process(self.bt_ls[n], self.at_ls[n], n))
        for n in range(self.processor_n):
            self.processor_ls.append(Processor())

    # DTRR 멀티코어 프로세싱
    def multicore_processing(self):
        time = 0;
        terminate = 0
        while (terminate != self.process_n):
            self.readyQueue.readyQue(self.process_ls, time)  # at에 예정된 프로세스 삽입
            for processor in self.processor_ls:
                if processor.process != None:
                    if processor.process.priority == LOW:  # 우선순위 별 TQ 조정
                        processor.time_progress_Lpriority(self.readyQueue)
                    elif processor.process.priority == MEDIUM:
                        processor.time_progress_Mpriority(self.readyQueue)
                    else:
                        processor.time_progress_Hpriority(self.readyQueue)
                # 시간 경과에 따른 제한시간(Time Quantum)처리

            time += 1
            for processor in self.processor_ls:
                # 큐에 프로세스가 있다면 비어있는 프로세서에 할당
                processor.ready_to_running(self.readyQueue)
                # 프로세서에 있는 프로세스 처리하기
                terminate += processor.running_process(time)
                # processor.time_progress(self.readyQueue)
        # 출력
        result = []
        for process in self.process_ls:
            result.append(
                [process.at, process.rbt, process.wt, process.tt, process.ntt])  # 실행이 종료된 프로세스의 속성을 값을 저장한 리스트
        p_memory = []
        for processor in self.processor_ls:
            p_memory.append(processor.processor_memory)  # 프로세서의 로그가 저장된 리스트
        return (result, p_memory)