from django.shortcuts import render
from .models import Process,Processor,Spn

# Create your views here.
def index(request):
    if request.method == "POST":
        if not request.POST["Process_name"] == "":
            # choose_scheduling_type(request)
            Spn(input_value(request)).mulitcore_processing()
        return render(request, 'index.html')
    return render(request, 'index.html')

def input_value(request):
    return [
        len(request.POST.getlist("Process_name")),
        int(request.POST['processor-number']),
        list(map(eval,request.POST['Burst_time'])),
        list(map(eval,request.POST['Arrive_time']))]

def choose_scheduling_type(request):
    if request.POST["scheduling-type"] == "FCFS":
        FCFS(input_value()).mulitcore_processing()
    elif request.POST["scheduling-type"] == "RR":
        RR(input_value()).mulitcore_processing()
    elif request.POST["scheduling-type"] == "SPN":
        Spn(input_value()).mulitcore_processing()
    elif request.POST["scheduling-type"] == "SRTN":
        SRTN(input_value()).mulitcore_processing()
    else :
        HRRN(input_value()).mulitcore_processing()