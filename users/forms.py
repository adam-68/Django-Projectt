from django import forms
from .models import CustomUser, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import datetime
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.exceptions import ValidationError


UserModel = get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200,
                             widget=forms.TextInput(attrs={'class': 'form-control input-lg',
                                                           'placeholder': "Email",
                                                           }))
    first_name = forms.CharField(max_length=30,
                                 widget=forms.TextInput(attrs={'class': 'form-control input-lg',
                                                               'placeholder': "First Name"}))
    last_name = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={'class': 'form-control input-lg',
                                                              "placeholder": "Last Name"}))
    birth_date = forms.DateField(initial=datetime.date.today(),
                                 widget=forms.widgets.DateInput(attrs={'type': 'date',
                                                                       'class': "form-control input-lg"}))
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': "form-control input-lg",
                                                             'placeholder': "Username"}))
    password1 = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(attrs={'class': "form-control input-lg",
                                                                  'placeholder': "Password"}))
    password2 = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(attrs={'class': "form-control input-lg",
                                                                  "placeholder": "Confirm Password"}))

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = UserCreationForm.Meta.fields + ('username', 'first_name','last_name', 'email', 'birth_date', 'password1', 'password2', )

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password1'])
    #     if commit:
    #         user.save()
    #     return user
    # def clean_email(self):
    #     email = self.cleaned_data['email'].lower()
    #     r = User.objects.filter(email=email)
    #     if r.count():
    #         raise ValidationError("User already exists.")
    #     return email
    #
    # def clean_birth_date(self):
    #     birth_date = self.cleaned_data['birth_date']
    #     age = (datetime.date.today() - birth_date).days/365
    #     if age < 13:
    #         raise ValidationError("You must be at least 13 years old to create an account.")
    #     return birth_date


class LoginForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     super(LoginForm, self).__init__(*args, **kwargs)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control input-lg',
                                                              'placeholder': "Email",
                                                              }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control input-lg",
                                               'placeholder': "Password"}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = UserModel.objects.get(email=email)
        if not user:
            raise forms.ValidationError("Invalid credentials - user does not exist")

        if not user.check_password(password):
            raise forms.ValidationError('Invalid credentials - wrong password or user.')
        return super(LoginForm, self).clean(*args, **kwargs)