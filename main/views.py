from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tutorial, TutorialCategory, TutorialSeries
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm
# Create your views here.

def single_slug(request, single_slug): #From urls.py
    """
    Determine if category or tutorial to see how many slashes to add
    .../category/tutorial vs .../category/
    """
    categories = [c.category_slug for c in TutorialCategory.objects.all()]
    if single_slug in categories:
        #Point at the series tutorial category's category slug
        #double __ is a points to b a__b
        matching_series = TutorialSeries.objects.filter(tutorial_category__category_slug = single_slug)
        series_urls = {}
        #Returns all the tutorials that are a part of the series, showing earliest published tutorial
        for m in matching_series.all():
            part_one = Tutorial.objects.filter(tutorial_series__tutorial_series = m.tutorial_series).earliest('tutorial_published')
            series_urls[m] = part_one.tutorial_slug
        return render(request,
                      template_name = 'main/category.html',
                       context={"tutorial_series": matching_series, 
                       "part_ones": series_urls})
    tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
    if single_slug in tutorials:
        return HttpResponse(f"{single_slug} is a tutorial")
    
    return HttpResponse(f"{single_slug} does not correspond to anything")



def homepage(request):
    #Shows categories on home page
    return render(request = request, 
                template_name = 'main/categories.html',  
                context = {'categories': TutorialCategory.objects.all})
    #Template name adds on main/home.html to this file path

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save() #Creates user
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect('main:homepage')#Goes to urls.py, sees app_name, then goes to name homepage
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")

    form = NewUserForm
    return render(request,
                    "main/register.html",
                    context = {'form' : form}) #Name same thing, common practice
def logout_request(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('main:homepage')

def login_request(request):
    if request.method == 'POST': #Logs in
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid(): #check if form all filled out
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username,password =  password)
            if user is not None: #If those parameters exist
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect ('main:homepage')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password/ form filled incorrectly')
    form = AuthenticationForm()
    return render(request, 
                  'main/login.html',
                   {'form': form})