from django.shortcuts import render



def home_view(request):
    return render(request, 'base.html')

def discover_view(request):
    return render(request, 'discover.html')

def contact_view(request):
    return render(request, 'contact.html')

def about_view(request):
    return render(request, 'about.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')