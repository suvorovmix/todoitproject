from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Welcome back, @{}'.format(user.get_username()))
            return redirect('index')
        else:
            messages.error(request, 'Something is going wrong!')
            return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'GET':
        return render(request, 'accounts/register.html')
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        if '@' not in email:
            messages.error(request, 'Email is wrong!')
            return render(request, 'accounts/register.html')
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            try:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
            except Exception as err:
                messages.error(request, 'Something is going wrong! ({})'.format(err))
                return render(request, 'accounts/register.html')
            else:
                auth.login(request, user)
                messages.success(request, '@{}, We are happy to see you in TODOIT APP!'.format(user.get_username()))
                return redirect('index')
        else:
            messages.error(request, 'Passwords did not match!')
            return render(request, 'accounts/register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')