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




class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["travel_date", "number_of_travelers", "special_requests", "emergency_contact"]
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['travel_package', 'hotel', 'activity', 'rating', 'comment', 'images']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'type': 'range',
                'min': '1',
                'max': '5',
                'step': '1',
                'class': 'form-range',
                'id': 'ratingRange'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience...'
            }),
            'travel_package': forms.Select(attrs={'class': 'form-select'}),
            'hotel': forms.Select(attrs={'class': 'form-select'}),
            'activity': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional
        self.fields['travel_package'].required = False
        self.fields['hotel'].required = False
        self.fields['activity'].required = False
        self.fields['comment'].required = False
        self.fields['images'].required = False
        
        # Add labels
        self.fields['travel_package'].label = "Travel Package"
        self.fields['hotel'].label = "Hotel"
        self.fields['activity'].label = "Activity"
        self.fields['rating'].label = "Rating (1-5 stars)"
        self.fields['comment'].label = "Your Review"
        self.fields['images'].label = "Upload Images (Optional)"
    
    def clean(self):
        cleaned_data = super().clean()
        travel_package = cleaned_data.get('travel_package')
        hotel = cleaned_data.get('hotel')
        activity = cleaned_data.get('activity')
        
        # Ensure at least one of the review targets is set
        if not travel_package and not hotel and not activity:
            raise forms.ValidationError("Please select a travel package, hotel, or activity to review.")
        
        # Ensure only one of the review targets is set
        if sum([bool(travel_package), bool(hotel), bool(activity)]) > 1:
            raise forms.ValidationError("Please select only one item to review.")
        
        return cleaned_data