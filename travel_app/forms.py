from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from random import randint
from .models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove password validation messages
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


    def save(self, commit=True):
        user = super().save(commit=False)

        email = self.cleaned_data['email']
        username=email.split("@")[0] + str(randint(1,999))  # Get the part before @
        user.username = username  # Set the username

        if commit:
            user.save()  # Save the user to the database
        return user
    



# forms.py


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'first_name', 'middle_name', 'last_name', 'address', 'contact_number', 
            'date_of_birth', 'profile_picture', 'gender',  
            'preferred_payment_method'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }