from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username = forms.CharField(label="Username", max_length=64)
	password = forms.CharField(widget=forms.PasswordInput())

class SignupForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False)
	last_name = forms.CharField(max_length=30, required=False)
	email = forms.EmailField(max_length=254)

	class Meta:
			model = User
			fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
	
	def __init__(self):
		super(UserCreationForm, self).__init__()
		self.fields['username'].widget.attrs['placeholder'] = 'Username'
		self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
		self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
		self.fields['email'].widget.attrs['placeholder'] = 'Email'
		self.fields['password1'].widget.attrs['placeholder'] = 'Test'
		self.fields['password2'].widget.attrs['placeholder'] = 'Test2'
		for fieldname in ['username', 'password1', 'password2']:
			self.fields[fieldname].help_text = None
			# self.fields[fieldname].label = None
