from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.
def index(request):
	return render(request, 'index.html')