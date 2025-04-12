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
import logging
from django.urls import reverse
import hmac
import hashlib
import base64
from django.views.decorators.http import require_POST



logger = logging.getLogger('travel_app')


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


@login_required
def wishlist_view(request):
    # Get or create wishlist for the user
    wishlist, created = WishList.objects.get_or_create(user=request.user)
    
    # Get all wishlist items
    wishlist_items = []
    
    # Add hotels
    for hotel in wishlist.hotels.all():
        wishlist_items.append({
            'id': hotel.id,
            'type': 'hotel',
            'name': hotel.name,
            'location': hotel.location,
            'price_per_night': str(hotel.price_per_night),
            'image': hotel.image.url if hotel.image else None
        })
    
    # Add activities
    for activity in wishlist.activities.all():
        wishlist_items.append({
            'id': activity.id,
            'type': 'activity',
            'name': activity.name,
            'location': getattr(activity, 'location', ''),
            'price': str(activity.price),
            'image': activity.image.url if activity.image else None
        })
    
    # Add packages
    for package in wishlist.packages.all():
        wishlist_items.append({
            'id': package.id,
            'type': 'package',
            'name': package.name,
            'location': package.location,
            'price': str(package.price),
            'image': package.image.url if package.image else None
        })
    
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist.html', context)

@login_required
@require_POST
def toggle_wishlist(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('id')
        item_type = data.get('type')
        
        # Get or create wishlist
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        
        # Handle different item types
        if item_type == 'hotel':
            item = Hotel.objects.get(id=item_id)
            if item in wishlist.hotels.all():
                wishlist.hotels.remove(item)
                added = False
            else:
                wishlist.hotels.add(item)
                added = True
                
        elif item_type == 'activity':
            item = Activity.objects.get(id=item_id)
            if item in wishlist.activities.all():
                wishlist.activities.remove(item)
                added = False
            else:
                wishlist.activities.add(item)
                added = True
                
        elif item_type == 'package':
            item = TravelPackage.objects.get(id=item_id)
            if item in wishlist.packages.all():
                wishlist.packages.remove(item)
                added = False
            else:
                wishlist.packages.add(item)
                added = True
        
        return JsonResponse({
            'status': 'success',
            'added': added,
            'removed': not added
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


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
    logger.debug(f"Payment initiated for booking ID: {booking.id}, Amount: {booking.total_amount}")
    
    payment, created = Payment.objects.get_or_create(
        booking=booking,
        defaults={
            'amount': booking.total_amount,
            'payment_method': 'eSewa',
            'payment_status': 'Pending'
        }
    )
    # eSewa form parameters (Epay-v1)
    esewa_data = {
        'amt': booking.total_amount,
        'pdc': 0,  # Delivery charge
        'psc': 0,  # Service charge
        'txAmt': 0,  # Tax amount
        'tAmt': booking.total_amount,
        'pid': f'booking_{booking.id}',
        'scd': settings.ESEWA_MERCHANT_ID,
        'su': request.build_absolute_uri(reverse('travel_app:payment_success', args=[booking.id])),
        'fu': request.build_absolute_uri(reverse('travel_app:payment_failure') + f'?booking_id={booking.id}'),
    }
    logger.info(f"eSewa payment form prepared for booking ID: {booking.id}, Parameters: {esewa_data}")
    return render(request, 'payment.html', {
        'booking': booking,
        'payment': payment,
        'esewa_data': esewa_data,
        'esewa_payment_url': settings.ESEWA_PAYMENT_URL,
    })

@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment = get_object_or_404(Payment, booking=booking)
    
    # Log query parameters received from eSewa
    oid = request.GET.get('oid')
    amt = request.GET.get('amt')
    refId = request.GET.get('refId')
    logger.debug(f"Payment success accessed for booking ID: {booking.id}, Query Params: oid={oid}, amt={amt}, refId={refId}")
    
    if oid and amt and refId:
        # Verify payment with eSewa
        try:
            verify_data = {
                'amt': float(amt),
                'scd': settings.ESEWA_MERCHANT_ID,
                'pid': oid,
                'rid': refId,
            }
            logger.debug(f"Sending verification request to eSewa: {verify_data}")
            response = requests.get(
                settings.ESEWA_VERIFY_URL,
                params=verify_data,
                headers={'User-Agent': 'Mozilla/5.0'},
            )
            logger.debug(f"eSewa verification response for booking ID: {booking.id}: {response.text}")
            
            if 'Success' in response.text:
                payment.transaction_id = refId
                payment.payment_status = 'Completed'
                payment.save()
                booking.payment_status = 'Paid'
                booking.status = 'Confirmed'
                booking.save()
                logger.info(f"Payment verified for booking ID: {booking.id}, Transaction ID: {refId}")
            else:
                payment.payment_status = 'Failed'
                payment.save()
                logger.warning(f"Payment verification failed for booking ID: {booking.id}: {response.text}")
                return redirect(reverse('travel_app:payment_failure') + f'?booking_id={booking.id}')
        except Exception as e:
            payment.payment_status = 'Failed'
            payment.save()
            logger.error(f"eSewa verification error for booking ID: {booking.id}: {str(e)}")
            return redirect(reverse('travel_app:payment_failure') + f'?booking_id={booking.id}')
        
        # Render the success page
        try:
            return render(request, 'payment_success.html', {'booking': booking, 'payment': payment})
        except Exception as e:
            logger.error(f"Template rendering error for booking ID: {booking.id}: {str(e)}")
            return redirect(reverse('travel_app:payment_failure') + f'?booking_id={booking.id}')
    else:
        logger.warning(f"Missing verification parameters for booking ID: {booking.id}: oid={oid}, amt={amt}, refId={refId}")
        payment.payment_status = 'Failed'
        payment.save()
        return redirect(reverse('travel_app:payment_failure') + f'?booking_id={booking.id}')

@login_required
def payment_failure(request):
    booking_id = request.GET.get('booking_id')
    booking = get_object_or_404(Booking, id=booking_id) if booking_id else None
    logger.debug(f"Payment failure accessed for booking ID: {booking_id or 'None'}")
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

