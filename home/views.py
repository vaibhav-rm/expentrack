from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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
        
        history.save()

        #update_balance(sender=History, instance=history, created=True)
        return redirect('/')
    queryset = History.objects.all().order_by('-id')[:5]
    queryset1 = Balance.objects.last()
    context = {'entries':queryset, 'balance':queryset1}
    return render(request, "home/index.html", context)

def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')
        
        user = authenticate(username = username, password = password)
        
        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/')
        
    return render(request, 'home/login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

def register_page(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password'] 

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request, 'Username already taken   ', extra_tags="alert notice")
            return redirect('/register/')
        
        user = User.objects.filter(email = email)

        if user.exists():
            messages.info(request, 'Email already exists', extra_tags="alert notice")
            return redirect('/register/')

        user = User.objects.create(
            username = username,
            email = email,
        )
        user.set_password(password)
        user.save()

        messages.info(request, 'Account created successfully', extra_tags="alert notice")

        return redirect('/register/')

    return render(request, 'home/register.html')

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
