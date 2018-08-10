from django import forms
from django.contrib.auth.models import User
from .models import Item, Profile, Cart

class LoginForm(forms.Form):
	username = forms.CharField(label="Username", max_length=64, widget=forms.TextInput(attrs={'placeholder':'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

class SellForm(forms.ModelForm):
	image = forms.ImageField()
	class Meta:
		model = Item
		fields = ['category', 'name', 'description', 'image', 'price', 'charity_percent']
		widgets = {
			'category': forms.TextInput(attrs={'class': 'category-hidden', 'hidden': True}),
			'name': forms.TextInput(attrs={'class': 'sell-name-input'}),
			'description': forms.Textarea(attrs={'class': 'sell-description-input'}),
			'price': forms.TextInput(attrs={'class': 'sell-price-input'}),
			'charity_percent': forms.TextInput(attrs={'class': 'charity-percent-hidden', 'hidden': True}),
		}

class ProfileUpdateForm(forms.ModelForm):
	image = forms.ImageField()
	class Meta:
		model = Profile
		fields = ['location', 'bio', 'image']
		widgets = {
			'location': forms.TextInput(attrs={'class': 'profile-location-input', 'placeholder': 'ex: Seattle, WA'}),
			'bio': forms.Textarea(attrs={'class': 'profile-bio-input'})
		}
