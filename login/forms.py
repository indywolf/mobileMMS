from django import forms

class LoginForm(forms.Form):
    Email = forms.EmailField()
    Password = forms.CharField(widget=forms.PasswordInput)

class ForgotForm(forms.Form):
    Email = forms.EmailField()
    FirstName = forms.CharField()