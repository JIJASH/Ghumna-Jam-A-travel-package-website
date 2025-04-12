from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import CustomerForm
from .models import *
from django.shortcuts import render, get_object_or_404
from .forms import BookingForm, ReviewForm
import requests
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests
import json





# @login_required
def home(request):
    destinations = Destination.objects.all()
    hotels = Hotel.objects.all()
    activities = Activity.objects.all()
    packages = TravelPackage.objects.all()
    
    context = {
        'destinations': destinations,
        'hotels': hotels,
        'activities': activities,
        'packages': packages,
    }
    return render(request, "home.html", context)




def authView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("travel_app:home")  
        else:
            print("Form errors:", form.errors)  
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
    reviews = Review.objects.all()
    return render(request, "review.html", {'reviews': reviews})


@login_required
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            
            # Handle the review_type radio button selection
            review_type = request.POST.get('review_type')
            
            # Clear all fields first
            review.travel_package = None
            review.hotel = None
            review.activity = None
            
            # Set only the selected field
            if review_type == 'travel_package':
                review.travel_package_id = request.POST.get('travel_package')
            elif review_type == 'hotel':
                review.hotel_id = request.POST.get('hotel')
            elif review_type == 'activity':
                review.activity_id = request.POST.get('activity')
            
            review.save()
            return redirect('travel_app:review')
    else:
        form = ReviewForm()
    
    # Get all available items for the dropdowns
    travel_packages = TravelPackage.objects.all()
    hotels = Hotel.objects.all()
    activities = Activity.objects.all()
    
    return render(request, 'submit_review.html', {
        'form': form,
        'travel_packages': travel_packages,
        'hotels': hotels,
        'activities': activities
    })







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

def package_detail(request, package_id):
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
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_confirmation.html', {'booking': booking})




@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment, created = Payment.objects.get_or_create(
        booking=booking,
        defaults={
            'amount': booking.total_amount,
            'payment_method': 'Khalti',
            'payment_status': 'Pending'
        }
    )
    if request.method == 'POST':
        return redirect('travel_app:payment_success', booking_id=booking.id)
    return render(request, 'payment.html', {'booking': booking, 'payment': payment})

@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment = get_object_or_404(Payment, booking=booking)
    token = request.GET.get('token')
    amount = request.GET.get('amount')
    if token and amount:
        try:
            headers = {
                'Authorization': f'Key {settings.KHALTI_SECRET_KEY}',
                'Content-Type': 'application/json',
            }
            payload = {
                'token': token,
                'amount': int(float(amount))  # Amount in paisa
            }
            response = requests.post(settings.KHALTI_VERIFY_URL, headers=headers, json=payload)
            response_data = response.json()
            if response.status_code == 200 and 'idx' in response_data:
                payment.transaction_id = response_data['idx']
                payment.khalti_token = token
                payment.khalti_status = response_data.get('state', {}).get('name', 'Completed')
                payment.payment_status = 'Completed'
                payment.save()
                booking.payment_status = 'Paid'
                booking.status = 'Confirmed'
                booking.save()
                return render(request, 'payment_success.html', {'booking': booking, 'payment': payment})
            else:
                payment.payment_status = 'Failed'
                payment.khalti_status = response_data.get('state', {}).get('name', 'Failed')
                payment.save()
                return redirect('travel_app:payment_failure')
        except Exception as e:
            payment.payment_status = 'Failed'
            payment.khalti_status = 'Error'
            payment.save()
            return redirect('travel_app:payment_failure')
    return render(request, 'payment_success.html', {'booking': booking, 'payment': payment})

@login_required
def payment_failure(request):
    booking_id = request.GET.get('booking_id')
    booking = get_object_or_404(Booking, id=booking_id) if booking_id else None
    return render(request, 'payment_failure.html', {'booking': booking})


@login_required
def like_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    # Get or create a set of liked reviews in the session
    liked_reviews = request.session.get('liked_reviews', [])
    
    # Check if user has already liked this review
    if str(review_id) in liked_reviews:
        # Unlike the review
        review.likes = max(0, review.likes - 1)  # Ensure likes don't go below 0
        review.save()
        liked_reviews.remove(str(review_id))
        request.session['liked_reviews'] = liked_reviews
        request.session.modified = True
        
        return JsonResponse({
            'likes_count': review.likes,
            'success': True,
            'action': 'unliked'
        })
    else:
        # Like the review
        review.likes += 1
        review.save()
        liked_reviews.append(str(review_id))
        request.session['liked_reviews'] = liked_reviews
        request.session.modified = True
        
        return JsonResponse({
            'likes_count': review.likes,
            'success': True,
            'action': 'liked'
        })

