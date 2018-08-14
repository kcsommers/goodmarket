from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Item, Profile, Cart, Charity, Review
from django.contrib import messages 
from .forms import LoginForm, SellForm, ProfileUpdateForm, SignUpForm, ReviewForm
from django.core.mail import send_mail
import cloudinary.uploader
import cloudinary.api
import requests
import stripe
import random
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
	subtotal = int(float(request.POST.get("subtotal")) * 100)
	charity_sum = int(float(request.POST.get("charity_sum")) * 100)
	transfer_group = request.user.username + str(random.random())

	charge = stripe.Charge.create(
		amount=subtotal,
		currency="usd",
		source=request.POST.get("stripeToken")
	)

	buyer_profile = Profile.objects.get(user=request.user)
	itemIds = request.POST.getlist("item_id")
	# prices = request.POST.getlist("item_price")
	charities = request.POST.getlist("charity_id")
	# charity_percentages = request.POST.getlist("charity_percent")
	sellers = request.POST.getlist("user_id")

	for i in range(len(sellers)):
		# get each item, mark it sold
		item = Item.objects.get(id=itemIds[i])
		item.sold = True
		item.save()

		# get the cart, remove the item
		cart = Cart.objects.get(user=request.user)
		cart.items.remove(item)

		# find the seller, get their stripe token
		seller = User.objects.get(id=sellers[i])
		profile = Profile.objects.get(user=seller)
		token = profile.stripe_user_id

		# subtract amount that will go to charity
		amount_to_seller = float(item.price) - float(item.price) * (float(item.charity_percent) / 100)
		amount_to_seller = int(amount_to_seller * 100)

		# get charity, update total money raised
		total_amount = int(float(item.price) * 100)
		charity_fee = total_amount - amount_to_seller
		charity = Charity.objects.get(id=charities[i])
		############# Remove Division If Non-Functional !!
		charity.total_money_raised += (charity_fee / 100 )
		charity.save()

		# update seller donation totals
		profile.charity += charity_fee
		profile.save()

		# transfer funds to appropraite seller accounts
		transfer = stripe.Transfer.create(
			amount=amount_to_seller,
			currency="usd",
			destination=token,
			source_transaction=charge.id
		)

		# send email to seller
		subject = 'Your item has sold!'
		from_email = settings.EMAIL_HOST_USER
		to_email = [seller.email]
		html_message = '<h1>Thank you for selling with Goodmarket!</h1><br /><p>Your item, ' + item.name + ', was purchased by ' + request.user.username + '. ' + str(item.charity_percent) + '% of your price will be donated to ' + item.charity.name + '. The remaining amount will be deposited to your Stripe acount.<br /><br /><em>The Goodmarket Team</em></p>'
		text_message = 'Your item, ' + item.name + ', was purchased by ' + request.user.username + '. ' + str(item.charity_percent) + '% of your price will be donated to ' + item.charity.name + '. Thank you for sellings with us!'
		send_mail(subject=subject, message=text_message, html_message=html_message, from_email=from_email, recipient_list=to_email, fail_silently=False)

	# convert sellers array into query string (for email link)
	sellersStr = '?seller=' + ('&seller=').join(sellers)
	print('SELLERSSTRING', sellersStr)

	# send email to buyer
	subject = 'Thank you for using Goodmarket!'
	from_email = settings.EMAIL_HOST_USER
	to_email = [request.user.email]
	html_message = '<h1>Thank you for using Goodmarket!</h1><h3>Your order is being processed, and you will receive an emailed receipt from Stripe shortly.</h3><br /><p>Follow the link below to find seller contact information, and leave reviews.</p><br /><a href="http://localhost:8000/seller_info/' + sellersStr + '">Get Seller Information</a><br /><br /><em>The Goodmarket Team</em>'
	text_message = 'Thank you for using Goodmarket! Your order is being processed, and you will receive an emailed receipt from Stripe shortly.'
	send_mail(subject=subject, message=text_message, html_message=html_message, from_email=from_email, recipient_list=to_email, fail_silently=False)


	return HttpResponseRedirect("/")

	print('babababumbabum: ', charge)


# def checkout(request):
# 	print('EMAIL', request.user.email)
# 	seller = None
# 	profile = None
# 	charity = None
# 	token = None
# 	amount_to_seller = 0
# 	total_amount = 0
# 	application_fee = 0

# 	buyer_profile = Profile.objects.get(user=request.user)
# 	itemIds = request.POST.getlist("item_id")
# 	prices = request.POST.getlist("item_price")
# 	charities = request.POST.getlist("charity_id")
# 	charity_percentages = request.POST.getlist("charity_percent")
# 	sellers = request.POST.getlist("user_id")

# 	for i in range(len(sellers)):
# 		item = Item.objects.get(id=itemIds[i])
# 		item.sold = True
# 		item.save()

# 		cart = Cart.objects.get(user=request.user)
# 		cart.items.remove(item)

# 		seller = User.objects.get(id=sellers[i])
# 		profile = Profile.objects.get(user=seller)
# 		token = profile.stripe_user_id
# 		amount_to_seller = float(prices[i]) - float(prices[i]) * (float(charity_percentages[i]) / 100)
# 		amount_to_seller = int(amount_to_seller * 100)
# 		total_amount = int(float(prices[i]) * 100)
# 		application_fee = total_amount - amount_to_seller

# 		charity = Charity.objects.get(id=charities[i])
# 		charity.total_money_raised += application_fee
# 		charity.save()

# 		subject = 'Your item has sold!'
# 		from_email = settings.EMAIL_HOST_USER
# 		to_email = [seller.email]
# 		message = 'Your item, ' + item.name + ', was purchased by' + request.user.username + '.'
# 		send_mail(subject=subject, message=message, from_email=from_email, recipient_list=to_email, fail_silently=False)
# 		return HttpResponseRedirect("/")

# 	charge = stripe.Charge.create(
# 		amount= total_amount,
# 		application_fee=application_fee,
# 		currency="usd",
# 		source=request.POST.get("stripeToken"),
# 		receipt_email=request.user.email,
# 		destination={
# 			"account": token
# 		}
# 	)

# 	print('babababumbabum: ', charge)

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
		form = SignUpForm(request.POST)
		if(form.is_valid()):
			form.save()
			u = form.cleaned_data['username']
			p = form.cleaned_data['password1']
			user = authenticate(username=u, password=p)
			login(request, user)
			return HttpResponseRedirect('/profile/update/')
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
	print('CHRHID: ', request.POST)
	print('CHRHID: ', request.POST.get('charity'))
	if(form.is_valid()):
		charity = Charity.objects.get(name=request.POST.get('charity', None))
		item = form.save(commit=False)
		item.user = request.user
		item.charity = charity
		item.save()
		return HttpResponseRedirect('/market/')
	else:
		return HttpResponseRedirect('/sell/')

def profile_update(request):
	return render(request, 'profile_update.html', {'user': request.user, 'form': ProfileUpdateForm})

@login_required
def profile(request):
	try: 
		profile = Profile.objects.get(user=request.user)
		sellingItems = Item.objects.all().filter(user=request.user, sold=False)
		soldItems = Item.objects.all().filter(user=request.user, sold=True)
		try: 
			reviews = Review.objects.all().filter(seller=request.user)
		except:
			reviews = []
		return render(request, 'profile.html', {
			'user': request.user, 
			'profile': profile, 
			'selling_items': sellingItems, 
			'sold_items': soldItems, 
			'reviews': reviews
		})
	except:
		print('NO PROFILE')
		return HttpResponseRedirect('/profile/update/')

def get_profile(request, user_id):
	try: 
		profile = Profile.objects.get(user_id=user_id)
		selling_items = Item.objects.all().filter(user_id=user_id, sold=False)
		soldItems = Item.objects.all().filter(user_id=user_id, sold=False)
		seller = User.objects.get(id=user_id)
		print("SELLER:", seller)
		try: 
			reviews = Review.objects.all().filter(seller=seller)
			print("REVIEWS:", reviews)
		except:
			reviews = []
			print("REVIEWS:", reviews)
		return render(request, "profile.html", {
			"user": user_id, 
			"profile": profile, 
			"selling_items": selling_items, 
			"sold_items": soldItems,
			"reviews": reviews
		})
	except:
		print("NO PROFILE")
		return HttpResponseRedirect('/market/')

# @login_required
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
	charities = Charity.objects.all()
	return render(request, 'charity.html', {'charities': charities})

@login_required
def sell(request):
	charities = Charity.objects.all()
	try:
		profile = Profile.objects.get(user=request.user)
		if profile.stripe_user_id == None:
			has_stripe_id = False
		else:
			has_stripe_id = True
		return render(request, 'sell.html', {
			'form': SellForm, 
			'has_stripe_id': has_stripe_id, 
			'user': request.user,
			'key': public_key,
			'client_id': stripe_client_id,
			'charities': charities
			})
	except:
		has_stripe_id = False
		return render(request, 'sell.html', {
			'form': SellForm, 
			'has_stripe_id': has_stripe_id, 
			'user': request.user,
			'key': public_key,
			'client_id': stripe_client_id,
			'charities': charities
			})

@login_required
def cart(request):
	# Check for User's Stripe ID
	has_stripe_id = False
	try: 
		profile = Profile.objects.get(user=request.user)
		if profile.stripe_user_id == None:
			has_stripe_id = False
		else:
			has_stripe_id = True
	except: 
		has_stripe_id = False
	# Find Cart
	try: 
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
		has_cart = True
		return render(request, "cart.html", {
			"items": items,
			"subtotal": subtotal,
			"charity_sum": charity_sum,
			"percentage_to_charity": percentage_to_charity,
			"has_cart": has_cart,
			'has_stripe_id': has_stripe_id, 
			'user': request.user,
			'key': public_key,
			'client_id': stripe_client_id
		})
	except:
		has_cart = False
		return render(request, "cart.html", {
			"has_cart": has_cart,
			'has_stripe_id': has_stripe_id, 
			'user': request.user,
			'key': public_key,
			'client_id': stripe_client_id
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

def review(request, seller_id):
	if request.method == "POST":
		form = ReviewForm(request.POST)
		print(request.POST)
		if (form.is_valid()):
			# Handle Submit
			seller = User.objects.get(id=request.POST.get("seller_id"))
			review = form.save(commit=False)
			review.reviewer = request.POST.get("reviewer")
			review.seller = seller
			review.save()
			return HttpResponseRedirect('/')
		else:
			print("FORM IS INVALID")
			return HttpResponseRedirect('/')
	else:
		form = ReviewForm(request.POST)
		seller = User.objects.get(id=seller_id)
		return render(request, "review.html", {'form': form, "user": request.user, "seller": seller})

def seller_info(request):
	seller_ids = request.GET.getlist('seller')
	print('SELLER IDS: ', seller_ids)
	sellers = []
	profiles = []
	for i in range(len(seller_ids)):
		user = User.objects.get(id=int(seller_ids[i]))
		profile = Profile.objects.get(user=user)
		sellers.append(user)
		profiles.append(profile)

	return render(request, "seller_info.html", {"sellers": sellers, "profiles": profiles})