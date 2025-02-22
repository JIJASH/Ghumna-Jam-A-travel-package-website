from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static

from django.conf import settings



urlpatterns = [
    path("", home, name="home"),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("logout/", LogoutView.as_view(), name="logout"), 
    path("profile/", profile, name="profile"),  
    path("discover/", discover, name="discover"),  
    path("wishlist/", wishlist, name="wishlist"),  
    path("review/", review, name="review"),
 

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)