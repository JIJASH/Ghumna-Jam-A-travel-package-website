from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import CustomerForm
from .models import *




# @login_required
def home(request):
    return render(request, "home.html", {})



def authView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user

            # Log the user in automatically
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("travel_app:home")  # Redirect to the home page
        else:
            print("Form errors:", form.errors)  # Debug print for form errors
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def logout():
    pass



@login_required
def profile(request):
 
    customer, created = Customer.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()  
            return redirect('travel_app:profile')  
    else:
        # Populate the form with the existing customer data
        form = CustomerForm(instance=customer)

    return render(request, 'profile.html', {'form': form})


def discover(request):
    return render(request, "discover.html", {})


def wishlist(request):
    return render(request, "wishlist.html", {})


def review(request):
    return render(request, "review.html", {})
