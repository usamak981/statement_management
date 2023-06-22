from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # customize the form fields here
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        

class SignupForm(UserCreationForm):
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the form fields here
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
        # self.fields['password1'].help_text = 'Your password must contain at least 8 characters, can\'t be too similar to your other personal information, and can\'t be a commonly used password.'
        # self.fields['password2'].help_text = 'Enter the same password as above, for verification.'


    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1, self.instance)
        return password1
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
