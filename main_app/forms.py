from django import forms
from django.contrib.auth.models import User
from .models import Item, Profile, Cart

class LoginForm(forms.Form):
	username = forms.CharField(label="Username", max_length=64, widget=forms.TextInput(attrs={'placeholder':'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

class SignUpForm(forms.ModelForm):
	    """
	    A form that creates a user, with no privileges, from the given username and
	    password.
	    """
	    error_messages = {
	        'password_mismatch': ("The two password fields didn't match."),
	    }
	    username = forms.CharField(label=("Username"), widget=forms.TextInput(attrs={'class': 'signup-username', 'placeholder': 'Username'}))
	    password1 = forms.CharField(label=("Password"),
	        widget=forms.PasswordInput(attrs={'class': 'signup-p1', 'placeholder': 'Password'}))
	    password2 = forms.CharField(label=("Password confirmation"),
	        widget=forms.PasswordInput(attrs={'class': 'signup-p1', 'placeholder': 'Confirm Password'}),
	        help_text=("Enter the same password as above, for verification."))

	    class Meta:
	        model = User
	        fields = ("username", 'password1', 'password2')

	    def clean_password2(self):
	        password1 = self.cleaned_data.get("password1")
	        password2 = self.cleaned_data.get("password2")
	        if password1 and password2 and password1 != password2:
	            raise forms.ValidationError(
	                self.error_messages['password_mismatch'],
	                code='password_mismatch',
	            )
	        return password2

	    def save(self, commit=True):
	        user = super(SignUpForm, self).save(commit=False)
	        user.set_password(self.cleaned_data["password1"])
	        if commit:
	            user.save()

	        return user

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
