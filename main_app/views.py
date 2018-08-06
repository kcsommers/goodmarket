from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
import requests

# Create your views here.
def index(request):
	return render(request, 'index.html')

def login_view(request):
	if(request.method == 'POST'):
		form = LoginForm(request.POST)
		if(form.is_valid()):
			u = form.cleaned_data['username']
			p = form.cleaned_data['password']
			user = authenticate(username=u, password=p)
			if (user is not None):
				if (user.is_active):
					login(request, user)
					print("LOGGED In")
					return HttpResponseRedirect('/')
				else:
					print("Account Disabled")
					return HttpResponseRedirect('/login/')
			else:
				return HttpResponseRedirect('/login/')
				print("Username and/or password is incorrect")
	else:
		form = LoginForm()
		return render(request, 'login.html', {'form': form})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')