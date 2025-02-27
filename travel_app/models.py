from django.db import models
from django.contrib.auth.models import AbstractUser,Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password
from random import randint
from django.contrib.auth.models import User





from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        # Generate a unique username from the email
        username = email.split("@")[0] +  str(randint(1,9999))  # Example: john_abcd
        user = self.model(email=email, username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email





class Customer(models.Model):
    
    first_name=models.CharField(max_length=50,blank=True,null=True)
    middle_name=models.CharField(max_length=50,blank=True,null=True)
    last_name=models.CharField(max_length=50,blank=True,null=True)
    address=models.CharField(max_length=50,blank=True,null=True)
    contact_number=models.CharField(max_length=20,blank=True,null=True)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    
    MALE_CHOICE='M'
    FEMALE_CHOICE='F'
    OTHER_CHOICE='O'
    
    GENDER_CHOICES=[
        ('M','MALE'),
        ('F','FEMALE'),
        ('O','OTHER'),
    ]
    
    gender=models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True, null=True
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="customer")
    loyalty_points = models.PositiveIntegerField(default=0)
    preferred_payment_method = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"





class TourGuide(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField()
    experience_years = models.PositiveIntegerField()
    languages = models.JSONField(default=list)
    specialties = models.JSONField(default=list)
    certification = models.FileField(upload_to='guide_certifications/', blank=True, null=True)
    availability_status = models.BooleanField(default=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Guide: {self.user.username}"





class Hotel(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=dict, blank=True)  # Example: {"wifi": True, "pool": False}
    contact_number=models.CharField(max_length=20,blank=True,null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True, help_text="The hotel's website URL : https://www.hotelwebsite.com")  # Example: "https://www.hotelwebsite.com"
    check_in_time = models.TimeField(default='14:00')
    check_out_time = models.TimeField(default='12:00')
    total_rooms = models.PositiveIntegerField(default=0)
    available_rooms = models.PositiveIntegerField(default=0)
    rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)], blank=True, null=True,
        help_text="Hotel rating from 1.0 to 5.0 stars"
    )
    image=models.ImageField(upload_to='hotel_images/',blank=True,null=True)
    room_types = models.JSONField(default=dict)  # {"standard": 10, "deluxe": 5, "suite": 2}

    def __str__(self):
        return self.name

    def clean(self):
        if self.available_rooms > self.total_rooms:
            raise ValidationError("Available rooms cannot exceed total rooms")





class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.DurationField()
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('difficult', 'Difficult')]
    )
    min_participants = models.PositiveIntegerField(default=1)
    max_participants = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    equipment_provided = models.JSONField(default=list, help_text='Example: ["helmet", "harness", "ropes"]')
    safety_guidelines = models.TextField()
    image=models.ImageField(upload_to='activity_images/',blank=True,null=True)


    def __str__(self):
        return self.name





class TravelPackage(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    available_from=models.DateField()
    available_to=models.DateField()
    location=models.CharField(max_length=255,blank=True,null=True)
    features = models.JSONField(default=dict)
    duration = models.PositiveIntegerField(help_text="Duration in days", default=1)
    max_participants = models.PositiveIntegerField(default=10)
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('difficult', 'Difficult')],
        default='moderate'
    )
    included_services = models.JSONField(default=dict)
    excluded_services = models.JSONField(default=dict)
    meeting_point = models.CharField(max_length=255, blank=True, null=True)
    image=models.ImageField(upload_to='travelpackage_images/',blank=True,null=True)
    hotels = models.ManyToManyField(Hotel, related_name='travel_packages', blank=True)
    activities = models.ManyToManyField(Activity, related_name='travel_packages')
    tour_guide = models.ForeignKey(TourGuide, on_delete=models.SET_NULL, null=True, blank=True)
    cancellation_policy = models.TextField(default="Standard 24-hour cancellation policy applies")
    
    def __str__(self):
        return self.name
    
    def get_seasonal_price(self, date):
        seasonal_price = self.seasonal_prices.filter(start_date__lte=date, end_date__gte=date).first()
        return seasonal_price.price if seasonal_price else self.price

    def clean(self):
        if self.available_from > self.available_to:
            raise ValidationError("Available from date must be before available to date")








class SeasonalPrice(models.Model):
    travel_package = models.ForeignKey(
        TravelPackage, on_delete=models.CASCADE, related_name="seasonal_prices"
    )
    season = models.CharField(max_length=50)  # e.g., "Winter", "Summer", "Christmas"
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.season} Price for {self.travel_package.name}"

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date must be before end date")





class Booking(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
        ("Completed", "Completed"),
    ]
    PAYMENT_STATUS_CHOICES = [
        ("Unpaid", "Unpaid"),
        ("Partially Paid", "Partially Paid"),
        ("Paid", "Paid"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bookings")
    travel_package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE, related_name="bookings", blank=True, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="bookings", blank=True, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="bookings", blank=True, null=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="Unpaid")
    travel_date = models.DateField()
    number_of_travelers = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)    
    cancellation_reason = models.TextField(blank=True, null=True)
    emergency_contact = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"Booking by {self.customer.user.username} for {self.travel_package or self.hotel or self.activity}"





class Payment(models.Model):
    
    PAYMENT_METHOD_CHOICES=[
        ("ESEWA","ESEWA"),
        # ("Khalti","Khalti"),
        # ("Google Pay","Google Pay"),
        # ("Bank Transfer","Bank Transfer"),
        ("Credit Card", "Credit Card"),
        
    ]    
    PAYMENT_STATUS_CHOICES=[
        ("Pending","Pending"),
        ("Processing", "Processing"),
        ("Completed","Completed"),
        ("Failed","Failed"),
        ("Refunded", "Refunded")
    ]
    booking=models.OneToOneField(Booking,on_delete=models.CASCADE,related_name="payment")
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    payment_date=models.DateTimeField(auto_now_add=True)
    payment_method=models.CharField(max_length=20,choices=PAYMENT_METHOD_CHOICES)
    payment_status=models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES,default="Pending")
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_proof = models.FileField(upload_to='payment_proofs/', blank=True, null=True)
    refund_status = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"Payment for booking {self.booking.id}"





class Review(models.Model):
   
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="reviews")
    travel_package=models.ForeignKey(TravelPackage, on_delete= models.CASCADE , related_name="reviews")
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment=models.TextField(blank=True,null=True)
    review_date=models.DateTimeField(auto_now_add=True)
    reply=models.TextField(blank=True,null=True)
    reply_date = models.DateTimeField(blank=True, null=True)
    images = models.ImageField(upload_to='review_images/', blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.travel_package.name}"





class WishList(models.Model):
    
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="wishlist")
    travel_package=models.ForeignKey(TravelPackage, on_delete= models.CASCADE , related_name="wishlist")
    added_date=models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['user', 'travel_package']
    
    def __str__(self):
        return f"Wishlist item for {self.user.username}: {self.travel_package.name}"
    



class Destination(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the destination")
    description = models.TextField(help_text="Brief description of the destination")
    location = models.CharField(max_length=255, help_text="Location of the destination (e.g., city, country)")
    image = models.ImageField(upload_to='destination_images/', blank=True, null=True, help_text="Image of the destination")
    best_time_to_visit = models.CharField(max_length=255, blank=True, null=True, help_text="Best time to visit the destination")
    climate = models.CharField(max_length=255, blank=True, null=True, help_text="Climate of the destination")
    popular_attractions = models.JSONField(default=list, blank=True, help_text="List of popular attractions (e.g., ['Pashupatinath', 'Boudhanath Stupa'])")

    hotels = models.ManyToManyField(Hotel, related_name='destinations', blank=True, help_text="Hotels available in this destination")
    activities = models.ManyToManyField(Activity, related_name='destinations', blank=True, help_text="Activities available in this destination")
    travel_packages = models.ManyToManyField(TravelPackage, related_name='destinations', blank=True, help_text="Travel packages available for this destination")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"


