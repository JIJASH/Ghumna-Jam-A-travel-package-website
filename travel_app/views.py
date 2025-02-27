from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import CustomerForm
from .models import *
from django.shortcuts import render, get_object_or_404





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
    destinations = Destination.objects.all()
    return render(request, "discover.html", {"destinations": destinations})


def destination_detail(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    return render(request, "destination_detail.html", {"destination": destination})


def wishlist(request):
    return render(request, "wishlist.html", {})


def review(request):
    return render(request, "review.html", {})


def search_all(request):
    return render(request, "search_all.html", {})




def hotels(request):

    hotels = Hotel.objects.all()
    return render(request, "hotels.html", {"hotels": hotels})



def hotel_detail(request, hotel_id):
    
    hotel = get_object_or_404(Hotel, id=hotel_id)
    return render(request, "hotel_detail.html", {"hotel": hotel})




def activity(request):
    activities = Activity.objects.all()
    return render(request, "activity.html", {"activities": activities})

def activity_detail(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    return render(request, "activity_detail.html", {"activity": activity})

def packages(request):
    packages = TravelPackage.objects.all()
    return render(request, "packages.html", {"packages": packages})

def package_datail(request, package_id):
    package = get_object_or_404(TravelPackage, id=package_id)
    return render(request, "package_detail.html", {"package": package})