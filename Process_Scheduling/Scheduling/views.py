from django.shortcuts import render
from .models import Process,Processor,Spn

# Create your views here.
def index(request):
    result = [['0','3','-','-','-'],['1','7','-','-','-',],['3','2','-','-','-',],['5','5','-','-','-',],['6','3','-','-','-',]]
    if request.method == "POST":
        if not request.POST["Burst_time"] == "":
            # choose_scheduling_type(request)
            print(request.POST)
            result = Spn(input_value(request)).mulitcore_processing()
            return render(request, 'index.html', {'results':result})
    print(result)
    return render(request, 'index.html',{'results':result})

def input_value(request):
    return [
        len(request.POST.getlist("Burst_time")),
        int(request.POST['processor-number']),
        list(map(eval,request.POST.getlist('Burst_time'))),
        list(map(eval,request.POST.getlist('Arrive_time')))]

def choose_scheduling_type(request):
    if request.POST["scheduling-type"] == "FCFS":
        FCFS(input_value()).mulitcore_processing()
    elif request.POST["scheduling-type"] == "RR":
        RR(input_value()).mulitcore_processing()
    elif request.POST["scheduling-type"] == "SPN":
        Spn(input_value()).mulitcore_processing()
    elif request.POST["scheduling-type"] == "SRTN":
        SRTN(input_value()).mulitcore_processing()
    elif request.POST["scheduling-type"] == "HRRN":
        HRRN(input_value()).mulitcore_processing()