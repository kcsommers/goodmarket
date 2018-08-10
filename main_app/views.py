from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Item, Profile, Cart
from django.contrib import messages 
from .forms import LoginForm, SellForm, SignUpForm, ProfileUpdateForm
import cloudinary.uploader
import cloudinary.api
import requests
import stripe
from django.db.models import Sum
from decimal import Decimal
stripe_secret_key = getattr(settings, "STRIPE_SECRET_KEY", None)
stripe.api_key = stripe_secret_key
public_key = getattr(settings, "STRIPE_PUBLISHABLE_KEY", None)
stripe_client_id = getattr(settings, "STRIPE_CLIENT_ID", None)

# Create your views here.
def index(request):
	return render(request, 'index.html', {'user': request.user, 'key': public_key, 'client_id': stripe_client_id})

def market(request):
	items = Item.objects.all()
	return render(request, 'market.html', {"items": items})

def checkout(request):
	print('CHECKOUT', request)
	profile = Profile.objects.get(user=request.user)
	connected_account = profile.stripe_user_id
	if(request.method == "POST"):
		charge = stripe.Charge.create(
			amount=100,
			currency="usd",
			source=request.POST['stripeToken'],
			destination={
				"account": connected_account
			}
		)
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
	if(request.method == 'POST'):
		form = SignUpForm(request.POST);
		if(form.is_valid()):
			form.save()
			return HttpResponseRedirect('/post_profile')
		else: 
			return HttpResponseRedirect("/")
			print("Invalid Information")
	else:
		form = SignUpForm
		return render(request, "signup.html", {"form": form})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def show_item(request, item_id):
		item = Item.objects.get(id=item_id)
		return render(request, 'show.html', {'item': item})

@login_required
def post_item(request):
	form = SellForm(request.POST, request.FILES)
	if(form.is_valid()):
		item = form.save(commit=False)
		item.user = request.user
		item.save()
		return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/sell/')

@login_required
def profile_update(request):
	return render(request, 'profile_update.html', {'user': request.user, 'form': ProfileUpdateForm})

@login_required
def profile(request):
	try: 
		profile = Profile.objects.get(user=request.user)
		sellingItems = Item.objects.all().filter(user=request.user, sold=False)
		soldItems = Item.objects.all().filter(user=request.user, sold=True)
		return render(request, 'profile.html', {'user': request.user, 'profile': profile, 'selling_items': sellingItems, 'sold_items': soldItems})
	except:
		print('NO PROFILE')
		return HttpResponseRedirect('/profile/update/')

@login_required
def post_profile(request):
	form = ProfileUpdateForm(request.POST, request.FILES)
	if(form.is_valid()):
		print("######ITS VALID")
		profile, created = Profile.objects.update_or_create(user_id=request.user.id, defaults={**form.cleaned_data, 'user': request.user})
		return HttpResponseRedirect('/profile/')
	else:
		print('NOT VALID')
		return HttpResponseRedirect('/profile/update')

def charity(request):
	return render(request, 'charity.html')

@login_required
def sell(request):
	return render(request, 'sell.html', {'form': SellForm})

@login_required
def cart(request):
	# Find Cart
	cart = Cart.objects.get(user=request.user)
	# Find Items in Cart
	items = cart.items.values()
	# Cart Subtotal
	subtotal = 0
	# Dollar Amount to Charity
	charity_sum = 0
	for item in items:
		subtotal += item["price"]
		charity_sum += item["price"] * item["charity_percent"]
	charity_sum = charity_sum / 100
	# Percentage of Cart Value Going to Charity
	percentage_to_charity = charity_sum * 100
	percentage_to_charity = round(percentage_to_charity / subtotal, 1)
	return render(request, "cart.html", {
		"items": items,
		"subtotal": subtotal,
		"charity_sum": charity_sum,
		"percentage_to_charity": percentage_to_charity
})

def thecart(request, item_id):
	item = Item.objects.get(id=item_id)
	cart, created = Cart.objects.get_or_create(user=request.user, defaults={
		"user": request.user
	})
	cart.items.add(item)
	return HttpResponseRedirect("/cart/")

def stripe_redirect(request):
	auth_code = request.GET.get('code')
	user_id = request.GET.get('state')
	user = User.objects.get(id=user_id)
	profile = Profile.objects.get(user=user)
	print('USERPROFILE', profile)
	print('AUTH_CODE', auth_code)
	url = 'https://connect.stripe.com/oauth/token'
	payload = {
		'client_secret': stripe_secret_key,
		'code': auth_code,
		'grant_type': 'authorization_code'
	}
	stripe_response = requests.post(url, data=payload)
	stripe_user_id = stripe_response.json()['stripe_user_id']
	print('STRIPE_USER_ID: ', stripe_user_id)
	profile.stripe_user_id = stripe_user_id
	profile.save()
	return HttpResponseRedirect('/')

def cart_delete(request, item_id):
	item = Item.objects.get(id=item_id)
	cart = Cart.objects.get(user=request.user)
	cart.items.remove(item)
	return HttpResponseRedirect("/cart/")
