from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages


# Create your views here.

def profile(request):
    return render(request, 'index.html')


def error_page(request):
    return render(request, 'error_page.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request)
            return redirect('list_event_managers')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html', {'form': LoginForm})


class LoginView(LoginView):
    model = User
    form_class = LoginForm
    template_name = 'accounts/login.html'

# def index(request):
# return render(request, 'index.html')
