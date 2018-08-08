from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Item, Profile
from .forms import LoginForm, SignupForm
import requests
import stripe
stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", None)
public_key = getattr(settings, "STRIPE_PUBLISHABLE_KEY", None)
# stripe.api_key = "sk_test_nZ8qHYKUMpN53f0JNPYtvw7B"

# Create your views here.
def index(request):
	return render(request, 'index.html', {'key': public_key})

def market(request):
	items = Item.objects.all()
	return render(request, 'market.html', {"items": items})

def checkout(request):
	print('CHECKOUT', request)

	if(request.method == "POST"):
		charge = stripe.Charge.create(
			amount=100,
			currency="usd",
			source=request.POST['stripeToken']
		)
		print('#####################################', charge)
		return HttpResponseRedirect('/')

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

def signup_view(request):
	print("HIT SIGNUP ROUTE")
	if(request.method == 'POST'):
		print("REQUEST WAS POST")
		form = SignupForm(request.POST)
		if form.is_valid():
			print("FORM WAS VALID")
			form.save()
			u = form.cleaned_data.get('username')
			p = form.cleaned_data.get('password1')
			user = authenticate(username=u, password=p)
			login(request, user)
			print("SIGNED UP")
			return HttpResponseRedirect('/')
		else: 
			return HttpResponseRedirect("/")
			print("Invalid Information")
	else:
		form = SignupForm()
		return render(request, "signup.html", {"form": form})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def show_item(request, item_id):
	item = Item.objects.get(id=item_id)
	return render(request, 'show.html', {'item': item})

def charity(request):
	return render(request, 'charity.html')

def sell(request):
	return render(request, 'sell.html')