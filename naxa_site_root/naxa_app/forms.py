from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )


class ProfileForm(forms.ModelForm):
    country = forms.CharField(max_length=20)
    bio = forms.CharField(max_length=50)
    phonenumber = forms.CharField(max_length=10)
    interest = forms.CharField(max_length=50)
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    home_location = forms.CharField(
        help_text='Required Coordinates. Format: 27.690069,85.335646 Lat,Long')
    office_location = forms.CharField(
        help_text='Required Coordinates. Format: 27.685948,85.33498 Lat,Long')

    class Meta:
        model = User
        fields = ('country', 'bio', 'phonenumber', 'interest',
                  'birth_date', 'home_location', 'office_location', )
