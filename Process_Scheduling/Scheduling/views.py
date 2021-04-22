from django.shortcuts import render
from .models import Process,Processor,Spn

# Create your views here.
def index(request):
    print(request)
    # result = Spn().mulitcore_processing()

    return render(request, 'index.html')