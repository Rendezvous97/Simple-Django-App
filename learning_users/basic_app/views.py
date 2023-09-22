from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(requests):
    return render(requests, 'basic_app/index.html')

@login_required
def user_logout(requests):
    logout(requests)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(requests):
    logout(requests)
    return HttpResponse("You are logged in. Nice!")




def register(requests):

    registered=False

    if requests.method == "POST":
        user_form = UserForm(data = requests.POST)

        profile_form = UserProfileInfoForm(data = requests.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in requests.FILES:
                profile.profile_pic = requests.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(requests, 'basic_app/registration.html', 
                  context={
                      'user_form':user_form,
                      'registered':registered,
                      'profile_form':profile_form
                      })


def user_login(requests):

    if requests.method == "POST":
        username = requests.POST.get("username")
        password = requests.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(requests, user)
                return HttpResponseRedirect(reverse('index'))
            
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        
        else:
            print("Someone tried to login and failed!")
            print("Username: {username} and Password: {password}")
            return HttpResponse("Invalid login details supplied!")
    
    else:
        return render(requests, 'basic_app/login.html', {})