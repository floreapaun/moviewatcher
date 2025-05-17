from .models import Movie
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'watched_on', 'review']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'watched_on': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-2 border border-gray-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
        }


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
