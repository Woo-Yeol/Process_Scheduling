from django.shortcuts import render
from .models import Process,Processor,SPN,FCFS,RR,SRTN,HRRN,DTRR

# Create your views here.
def index(request):
    # 초기화면을 위한 result 초기화
    result = [['0','3','-','-','-'],
            ['1','7','-','-','-',],
            ['3','2','-','-','-',],
            ['5','5','-','-','-',],
            ['6','3','-','-','-',]]
    
    # POST 방식의 request를 확인하면
    if request.method == "POST":
        # 잘못된 입력값이 아닐경우
        if not request.POST["Burst_time"] == "":
            # 알맞은 알고리즘을 선택하고 프로세스 처리 결과를 저장한다.
            result = choose_scheduling_type(request)
            result, memory = result[0], choose_color(result[1])
            # 결과값으로 Render하기
            return render(request, 'index.html', {'results':result,'memory':memory})
    # 값이 입력되지 않았다면 초기 result 값을 Render한다.
    return render(request, 'index.html',{'results':result})

def choose_color(memory):
    color=["#f85a40", "#fbb034", "#ffdd00", "#c1d82f", "#00a4e4", "#6a67ce", "#fc636b",'#8a7967', '#6a737b', '#b4a996', '#c9c3e6','#f7afff','#d1de3f', '#f58268', '#8b8b64', '#87a6bc']
    for processor in range(len(memory)):
        for process in range(len(memory[processor])):
            if memory[processor][process] == 1:
                memory[processor][process] = (1,color[0])
            elif memory[processor][process] == 2:
                memory[processor][process] = (2,color[1])
            elif memory[processor][process] == 3:
                memory[processor][process] = (3,color[2])
            elif memory[processor][process] == 4:
                memory[processor][process] = (4,color[3])
            elif memory[processor][process] == 5:
                memory[processor][process] = (5,color[4])
            elif memory[processor][process] == 6:
                memory[processor][process] = (6,color[5])
            elif memory[processor][process] == 7:
                memory[processor][process] = (7,color[6])
            elif memory[processor][process] == 8:
                memory[processor][process] = (8,color[7])
            elif memory[processor][process] == 9:
                memory[processor][process] = (9,color[8])
            elif memory[processor][process] == 10:
                memory[processor][process] = (10,color[9])
            elif memory[processor][process] == 11:
                memory[processor][process] = (11,color[10])
            elif memory[processor][process] == 12:
                memory[processor][process] = (12,color[11])
            elif memory[processor][process] == 13:
                memory[processor][process] = (13,color[12])
            elif memory[processor][process] == 14:
                memory[processor][process] = (14,color[13])
            elif memory[processor][process] == 15:
                memory[processor][process] = (15,color[0])
    return memory
            

# 입력받은 값을 파이썬의 자료구조로 가공한다.
def input_value(request):
    return [
        len(request.POST.getlist("Burst_time")),
        int(request.POST['processor-number']),
        list(map(eval,request.POST.getlist('Burst_time'))),
        list(map(eval,request.POST.getlist('Arrive_time')))]

# 입력받은 스케줄링 기법을 확인하여 프로세스를 실행한다.
def choose_scheduling_type(request):
    if request.POST["scheduling-type"] == "FCFS":
        return FCFS(input_value(request)).multicore_processing()
    elif request.POST["scheduling-type"] == "RR":
        return RR(input_value(request), request.POST["TimeQuantum"]).multicore_processing()
    elif request.POST["scheduling-type"] == "SPN":
        return SPN(input_value(request)).multicore_processing()
    elif request.POST["scheduling-type"] == "SRTN":
        return SRTN(input_value(request)).multicore_processing()
    elif request.POST["scheduling-type"] == "HRRN":
        return HRRN(input_value(request)).multicore_processing()
    else:
        return DTRR(input_value(request)).multicore_processing()