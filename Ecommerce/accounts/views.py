from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from home.models import *
from django.contrib import messages


# Create your views here.
def user_login(request):
    if request.method == "POST":
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/accounts/index')
            messages.info(request, "incorrect password or username")
    return render(request, 'login.html')


def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        phone = request.POST.get('phone')
        if password == confirmPassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return redirect('/accounts/user_register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.info(request, "Email already exists")
                    return redirect('/accounts/user_register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    data = Customer(user=user, phone=phone)
                    data.save()
                    our_user = authenticate(username=username, password=password)
                    if our_user is not None:
                        login(request, user)
                        return redirect('/accounts/index')
        else:
            messages.info(request, "Miss matches password and confirm password")
            return redirect('/accounts/user_register')
    return render(request, 'registration.html')


def user_logout(request):
    logout(request)
    return redirect('/')


def index(request):
    return render(request, 'index.html')
