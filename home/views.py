from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import History
# Create your views here.


def index(request):
    if request.method == "POST":
        data = request.POST
        desc = data['desc']
        amount = data['amount']
        
        History.objects.create(
            desc=desc, 
            amount=amount,
        )
        return redirect('/')
    queryset = History.objects.all()
    context = {'entries':queryset}
    return render(request, "home/index.html", context)