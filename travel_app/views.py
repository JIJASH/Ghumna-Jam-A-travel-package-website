from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import CustomerForm
from .models import *
from django.shortcuts import render, get_object_or_404
from .forms import BookingForm
import requests
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse





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
            if 'type' in request.GET and 'id' in request.GET:
                return redirect('travel_app:booking', type=request.GET.get('type'), id=request.GET.get('id'))
            else:
                return redirect('travel_app:profile')
    else:
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


@login_required
def booking(request, type, id):
    customer = request.user.customer
    booking_item = None

    if type == "package":
        booking_item = get_object_or_404(TravelPackage, id=id)
    elif type == "hotel":
        booking_item = get_object_or_404(Hotel, id=id)
    elif type == "activity":
        booking_item = get_object_or_404(Activity, id=id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = customer

            if type == "package":
                booking.travel_package = booking_item
                booking.total_amount = booking_item.price * int(request.POST.get('number_of_travelers', 1))
            elif type == "hotel":
                booking.hotel = booking_item
                num_nights = 1  
                booking.total_amount = booking_item.price_per_night * num_nights
            elif type == "activity":
                booking.activity = booking_item
                booking.total_amount = booking_item.price * int(request.POST.get('number_of_travelers', 1))

            booking.save()
            return redirect('travel_app:payment', booking_id=booking.id)
        else:
            print("Form errors:", form.errors)
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form, 'booking_item': booking_item, 'type': type})



@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        # Handle payment logic here (e.g., integrate with a payment gateway)
        booking.payment_status = "Paid"
        booking.save()
        return redirect('travel_app:booking_confirmation', booking_id=booking.id)

    return render(request, 'payment.html', {'booking': booking})



@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_confirmation.html', {'booking': booking})




def payment_success(request):

    return render(request, 'booking_confirmation.html')

def payment_failure(request):
    return render(request, 'payment_failure.html')





# def initiate_payment(request, booking_id):
#     # Assuming you have a Booking model to fetch booking details
#     # Replace this with your actual Booking model
#     booking = Booking.objects.get(id=booking_id)  # Adjust based on your model

#     # Prepare the payload
#     payload = {
#         "return_url": "http://127.0.0.1:8000/payment-success/",
#         "website_url": "http://127.0.0.1:8000/",
#         "amount": str(int(booking.total_amount * 100)),  # Convert to paisa
#         "purchase_order_id": f"Order-{booking.id}",
#         "purchase_order_name": booking.travel_package.name if booking.travel_package else (booking.hotel.name if booking.hotel else booking.activity.name),
#         "customer_info": {
#             "name": "Test User",  # Replace with actual user data if available
#             "email": "test@khalti.com",
#             "phone": "9800000001"
#         }
#     }

#     # Khalti API endpoint (same for sandbox and live, determined by the key)
#     url = "https://khalti.com/api/v2/epayment/initiate/"

#     # Headers with your secret key
#     headers = {
#         "Authorization": "key live_secret_key_2b36142266e2a4cbcb4c0ea6f980913f",  # Replace with test secret key if available
#         "Content-Type": "application/json",
#     }

#     try:
#         # Make the POST request to Khalti
#         response = requests.post(url, headers=headers, data=json.dumps(payload))
#         response_data = response.json()

#         if response.status_code == 200 and "payment_url" in response_data:
#             # Redirect the user to Khalti's payment URL
#             return redirect(response_data["payment_url"])
#         else:
#             # Handle error
#             return HttpResponse(f"Payment initiation failed: {response.text}", status=400)

#     except Exception as e:
#         return HttpResponse(f"Error initiating payment: {str(e)}", status=500)

# def payment_success(request):
#     # Handle payment success (you can verify the payment here if needed)
#     return render(request, "payment_success.html", {"message": "Payment successful! Your booking has been confirmed."})

# def payment_failure(request):
#     return render(request, "payment_failure.html", {"message": "Payment failed. Please try again."})