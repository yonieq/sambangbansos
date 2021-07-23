from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return render(request, 'management/login.html')


def do_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        response = redirect('/management/dashboard/')
    else:
        response = redirect('/management/')
    return response


def do_logout(request):
    logout(request)
    response = redirect('/management/')
    return response


@login_required(login_url='/management/')
def dashboard(request):
    return render(request, 'management/dashboard.html')


