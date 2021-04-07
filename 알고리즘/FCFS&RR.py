import queue

class process:                    # 프로세스 클래스
  def __init__(self, AT, BT):
    self.AT = AT                  # 프로세스 객체의 AT 초기화
    self.BT = BT                  # 프로세스 객체의 BT 초기화
    self.num_CPU = None           # 프로세스에 배정된 CPU 정보
    self.burst_time = 0           # 프로세스 진행 시간
    self.waiting_time = 0         # 프로세스 WT
    self.turnaround_time = 0      # 프로세스 TT
    self.n_turnaround_time = 0    # 프로세스 NTT

  def setNum_CPU(self, n):        # 프로세스에 CPU 배정
    self.num_CPU = n

  def running(self):              # 프로세스 1s 진행
    self.burst_time += 1

  def setBurst_time(self, n):     # 프로세스 진행 시간 초기화
    self.burst_time = n
  
  def setWaiting_time(self, n):   # 프로세스 WT, TT, NTT 초기화
    self.waiting_time = n

  def setTurnaround_time(self, n):    
    self.turnaround_time = n

  def setN_turnaround_time(self, n):
    self.n_turnaround_time = n

class processor:                        # 프로세서 클래스
  def __init__(self, CPU_num):
    self.CPU_num = CPU_num              # 프로세서 정보
    self.is_working = False             # 프로세서 실행 중 여부
    self.working_process = None         # 프로세서에 할당된 프로세스 정보
    self.time_quantum = 0               # 프로세서 제한 시간

  def work(self):
    self.is_working = True              # 프로세서 실행

  def done(self):                       # 프로세서에 할됭된 프로세스 종료
    self.is_working = False             # 프로세서 실행 종료
    self.working_process = None         # 프로세스 할당 해제
    self.setTime_quantum(0)             # 프로세서 제한 시간 초기화

  def setWorking_process(self, p):      # 프로세서에 프로세스 할당
    self.working_process = p

  def running_CPU(self):                # 프로세서 1s 실행
    self.time_quantum += 1

  def setTime_quantum(self, n):         # 프로세서 제한 시간 초기화
    self.time_quantum = n

def FCFS(n_processor, n_process, AT, BT):   # FIRST - COME, FIRST - SERVICE

  process_list = []   # 프로세스 객체를 담을 list
  CPU_list = []       # 프로세서 객체를 담을 list
  Waiting = []        # 종료된 프로세서의 WT, TT, NTT를 담아 반환할 list
  TT = []             
  NTT = []
  time = 0            # 현재 진행 시간
  readyQueue = queue.Queue()    # ready Queue

  for i in range(n_process):                    # 입력 받은 만큼의 프로세스, 프로세서 객체를 생성해 리스트에 저장
    process_list.append(process(AT[i], BT[i]))
  for i in range(n_processor):
    CPU_list.append(processor(i))

  while(time <= sum(BT)):             # 최대 시간 = 모든 프로세스의 BT를 합친 시간 (더 효율적인 반복 종료 조건?)

    for now_process in process_list:  # 매 초마다 모든 프로세스 탐색
      if time == now_process.AT:      
        readyQueue.put(now_process)   # 설정된 AT에서 해당 프로세스를 readyQueue에 put

      if now_process.BT == now_process.burst_time:      # 프로세스의 현재 진행 시간이 BT가 되면
        CPU_list[now_process.num_CPU].done()            # 배정된 프로세서 종료
        now_process.setTurnaround_time(time - now_process.AT)   # 해당 프로세스의 WT, TT, NTT 계산
        now_process.setWaiting_time(now_process.turnaround_time - now_process.BT)   
        now_process.setN_turnaround_time(now_process.turnaround_time / now_process.BT)
        now_process.setBurst_time(0)    # 진행시간 초기화 => 안해주면 매 반복마다 해당 if절 실행됨

    for now_processor in CPU_list:    # 매 초마다 모든 프로세서 탐색
      if not now_processor.is_working and not readyQueue.empty():   # readyQueue가 비어있는데 프로세서가 실행중이지 않으면
        now_processor.setWorking_process(readyQueue.get())          # 큐에서 프로세스 하나를 꺼내서 배정
        now_processor.working_process.setNum_CPU(now_processor.CPU_num)   # 배정된 프로세스에 프로세서 정보 기입
        now_processor.work()    # 프로세서 실행

      if now_processor.working_process != None:   # 배정된 프로세스에 대해
        now_processor.working_process.running()   # 1s 만큼 진행 진행

    time += 1      # 1s 경과

  for done_process in process_list:               # 반복 종료 => 모든 프로세스 done
    Waiting.append(done_process.waiting_time)     # 계산된 WT, TT, NTT를 리스트에 담아
    TT.append(done_process.turnaround_time)
    NTT.append(done_process.n_turnaround_time)

  return Waiting, TT, NTT                         # 반환

def RR(n_processor, n_process, AT, BT, TQ):       # ROUND - ROBIN

  process_list = []   # 프로세스 객체를 담을 list
  CPU_list = []       # 프로세서 객체를 담을 list
  Waiting = []        # 종료된 프로세서의 WT, TT, NTT를 담아 반환할 list
  TT = []             
  NTT = []
  time = 0            # 현재 진행 시간
  readyQueue = queue.Queue()    # ready Queue

  for i in range(n_process):      # 입력 받은 만큼의 프로세스, 프로세서 객체를 생성해 리스트에 저장
    process_list.append(process(AT[i], BT[i]))
  for i in range(n_processor):
    CPU_list.append(processor(i))

  while(time <= sum(BT)):             # 최대 시간 = 모든 프로세스의 BT를 합친 시간 (더 효율적인 반복 종료 조건?)
    for now_process in process_list:  # 매 초마다 모든 프로세스 탐색
      if time == now_process.AT:
        readyQueue.put(now_process)   # 설정된 AT에서 해당 프로세스를 readyQueue에 put

    for now_process in process_list:  # FCFS와 다른점 => preemption이 발생하기 때문에 AT에서 큐에 넣는 작업 후 종료 작업 해야함  
      if now_process.BT == now_process.burst_time:                                          # 프로세스의 현재 진행 시간이 BT가 되면
        CPU_list[now_process.num_CPU].done()                                                # 배정된 프로세서 종료
        now_process.setTurnaround_time(time - now_process.AT)                               # 해당 프로세스의 WT, TT, NTT 계산
        now_process.setWaiting_time(now_process.turnaround_time - now_process.BT)
        now_process.setN_turnaround_time(now_process.turnaround_time / now_process.BT)
        now_process.setBurst_time(0)      # 진행시간 초기화 => 안해주면 매 반복마다 해당 if절 실행됨
        continue

    for now_processor in CPU_list:                      # CPU 제한 시간에 따른 Preemption 작업
      if now_processor.time_quantum == TQ:              # CPU가 제한 시간이 되면
        now_processor.working_process.setNum_CPU(-1)    # 배정된 프로세스 할당 해제에 따른 CPU 정보 초기화
        readyQueue.put(now_processor.working_process)   # 진행중이던 프로세스를 다시 큐에 넣음
        now_processor.done()                            # 프로세서 종료

    for now_processor in CPU_list:
      if not now_processor.is_working and not readyQueue.empty():         # readyQueue가 비어있는데 프로세서가 실행중이지 않으면
        now_processor.setWorking_process(readyQueue.get())                # 큐에서 프로세스 하나를 꺼내서 배정
        now_processor.working_process.setNum_CPU(now_processor.CPU_num)   # 배정된 프로세스에 프로세서 정보 기입
        now_processor.work()                                              # 프로세서 실행

      if now_processor.working_process != None:       # 배정된 프로세스에 대해
        now_processor.working_process.running()       # 1s 만큼 진행 진행
        now_processor.running_CPU()                   # CPU 제한시간 1s 경과

    time += 1     # 1s 경과

  for done_process in process_list:                   # 반복 종료 => 모든 프로세스 done
    Waiting.append(done_process.waiting_time)         # 계산된 WT, TT, NTT를 리스트에 담아
    TT.append(done_process.turnaround_time)
    NTT.append(done_process.n_turnaround_time)

  return Waiting, TT, NTT                         # 반환


def INPUT():

  n_process = eval(input("# of Processes : "))
  n_processor = eval(input("# of Processors : "))
  AT = list(map(int, input("Arrival time : ").split()))
  BT = list(map(int, input("Burst time : ").split()))

  return n_process, n_processor, list(AT), list(BT)

def INPUT_FOR_RR():
  n_process = eval(input("# of Processes : "))
  n_processor = eval(input("# of Processors : "))
  AT = list(map(int, input("Arrival time : ").split()))
  BT = list(map(int, input("Burst time : ").split()))
  TQ = eval(input("Time quantum for RR : "))

  return n_process, n_processor, list(AT), list(BT), TQ

def main():
  n_process, n_processor, AT, BT = INPUT()
  WT, TT, NTT = FCFS(n_processor, n_process, AT, BT)

  # n_process, n_processor, AT, BT, TQ = INPUT_FOR_RR()
  # WT, TT, NTT = RR(n_processor, n_process, AT, BT, TQ)

  print(WT)
  print(TT)
  print(NTT)

main()