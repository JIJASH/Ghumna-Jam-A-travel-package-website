from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static

from django.conf import settings



app_name = 'travel_app'

urlpatterns = [
    path("", home, name="home"),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("logout/", LogoutView.as_view(), name="logout"), 
    path("profile/", profile, name="profile"),  
    path("discover/", discover, name="discover"),
    path("destination/<int:destination_id>/", destination_detail, name="destination_detail"),  
    path("wishlist/", wishlist, name="wishlist"),  
    path("review/", review, name="review"),
    # path('search_all/', search_all, name='search_all'),
    path('hotels/', hotels, name='hotels'),
    path('hotel/<int:hotel_id>/', hotel_detail, name='hotel_detail'),
    path('activity/', activity, name='activity'),
    path("activity/<int:activity_id>/", activity_detail, name="activity_detail"),
    path('packages/', packages, name='packages'),
    path("packages/<int:package_id>/", package_detail, name="package_detail"),
    path("booking/<str:type>/<int:id>/", booking, name="booking"),
    path("booking_confirmation/<int:booking_id>/", booking_confirmation, name="booking_confirmation"),
    path("payment/<int:booking_id>/", payment, name="payment"),
    path("payment-success/", payment_success, name="payment_success"),
    path("payment-failure/", payment_failure, name="payment_failure"),
    
 

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)