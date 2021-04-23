from django.shortcuts import render
from .models import Process,Processor,SPN,FCFS,RR,SRTN,HRRN

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
            result, memory = result[0], result[1]
            # 결과값으로 Render하기
            return render(request, 'index.html', {'results':result,'memory':memory})
    # 값이 입력되지 않았다면 초기 result 값을 Render한다.
    return render(request, 'index.html',{'results':result})

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