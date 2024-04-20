from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
# Create your views here.


def index(request):
    if request.method == "POST":
        data = request.POST
        desc = data['desc']
        amount = int(data['amount'])
        
        history = History.objects.create(
            desc=desc, 
            amount=amount,
        )
        #update_balance(sender=History, instance=history, created=True)
        return redirect('/')
    queryset = History.objects.all().order_by('-id')[:5]
    queryset1 = Balance.objects.last()
    context = {'entries':queryset, 'balance':queryset1}
    return render(request, "home/index.html", context)

def delete_entry(request, id):
    history_entry = History.objects.get(id=id)
    amount_to_delete = history_entry.amount
    
    history_entry.delete()
    balance = Balance.objects.first() 
    
    if balance:
        balance.balance -= amount_to_delete
        if amount_to_delete > 0:
            balance.income -= amount_to_delete
        elif amount_to_delete < 0:
            balance.expense -= amount_to_delete
        balance.save()
    
    return redirect('/')
