from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tutorial
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def homepage(request):
    return render(request = request, 
                template_name = 'main/home.html', 
                context = {'tutorials': Tutorial.objects.all})
    #Template name adds on main/home.html to this file path

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() #Creates user
            login(request, user)
            return redirect('main:homepage')#Goes to urls.py, sees app_name, then goes to name homepage
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

    form = UserCreationForm
    return render(request,
                    "main/register.html",
                    context = {'form' : form}) #Name same thing, common practice