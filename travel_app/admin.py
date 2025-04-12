from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'contact_number', 'email', 'loyalty_points','profile_picture')
    list_filter = ('gender', 'preferred_payment_method')
    search_fields = ('first_name', 'last_name', 'email', 'contact_number')
    list_editable=('first_name', 'last_name', 'contact_number', 'email', 'loyalty_points','profile_picture')
    list_per_page = 20
    readonly_fields = ('loyalty_points',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth','profile_picture')
        }),
        ('Contact Details', {
            'fields': ('email', 'contact_number', 'address')
        }),
        ('Customer Profile', {
            'fields': ('loyalty_points', 'preferred_payment_method')
        })
    )


@admin.register(TourGuide)
class TourGuideAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience_years', 'hourly_rate', 'availability_status')
    list_filter = ('availability_status', 'experience_years')
    search_fields = ('user__username', 'specialties')
    list_editable = ('availability_status', 'hourly_rate')
    list_per_page = 20
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'bio', 'experience_years')
        }),
        ('Qualifications', {
            'fields': ('languages', 'specialties', 'certification')
        }),
        ('Work Details', {
            'fields': ('availability_status', 'hourly_rate')
        })
    )


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price_per_night', 'rating', 'available_rooms', 'total_rooms')
    list_filter = ('rating', 'location')
    search_fields = ('name', 'location', 'description')
    list_editable = ('price_per_night', 'available_rooms')
    list_per_page = 20
    fieldsets = (
        ('Hotel Information', {
            'fields': ('name', 'location', 'description', 'image')
        }),
        ('Room Details', {
            'fields': ('total_rooms', 'available_rooms', 'room_types', 'price_per_night')
        }),
        ('Amenities & Features', {
            'fields': ('features', 'rating')
        }),
        ('Contact Information', {
            'fields': ('contact_number', 'email', 'website')
        }),
        ('Timings', {
            'fields': ('check_in_time', 'check_out_time')
        })
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'difficulty_level', 'price', 'min_participants', 'max_participants','image')
    list_filter = ('difficulty_level',)
    search_fields = ('name', 'description')
    list_editable = ('price',)
    list_per_page = 20
    fieldsets = (
        ('Activity Details', {
            'fields': ('name', 'description', 'image',  'duration', 'difficulty_level')
        }),
        ('Participation', {
            'fields': ('min_participants', 'max_participants', 'price')
        }),
        ('Equipment & Safety', {
            'fields': ('equipment_provided', 'safety_guidelines')
        })
    )


@admin.register(TravelPackage)
class TravelPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price', 'duration', 'difficulty_level')
    list_filter = ('difficulty_level', 'available_from', 'available_to')
    search_fields = ('name', 'location', 'description')
    list_editable = ('price',)
    filter_horizontal = ('hotels', 'activities')
    list_per_page = 20
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'location', 'image')
        }),
        ('Availability & Pricing', {
            'fields': ('price', 'available_from', 'available_to', 'duration')
        }),
        ('Package Details', {
            'fields': ('difficulty_level', 'max_participants', 'meeting_point')
        }),
        ('Services', {
            'fields': ('included_services', 'excluded_services', 'features')
        }),
        ('Relationships', {
            'fields': ('hotels', 'activities', 'tour_guide')
        }),
        ('Policies', {
            'fields': ('cancellation_policy',)
        })
    )


@admin.register(SeasonalPrice)
class SeasonalPriceAdmin(admin.ModelAdmin):
    list_display = ('travel_package', 'season', 'start_date', 'end_date', 'price', 'discount_percentage')
    list_filter = ('season', 'start_date', 'end_date')
    search_fields = ('season', 'travel_package__name')
    list_editable = ('price', 'discount_percentage')
    list_per_page = 20


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'travel_package', 'booking_date', 'travel_date', 'status', 'payment_status', 'total_amount')
    list_filter = ('status', 'payment_status', 'booking_date', 'travel_date')
    search_fields = ('customer__first_name', 'travel_package__name')
    readonly_fields = ('booking_date', 'total_amount')
    list_per_page = 20
    fieldsets = (
        ('Booking Information', {
            'fields': ('customer', 'travel_package', 'travel_date', 'number_of_travelers')
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
        }),
        ('Additional Details', {
            'fields': ('special_requests', 'emergency_contact', 'cancellation_reason')
        }),
        ('Financial', {
            'fields': ('total_amount',)
        })
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_date', 'payment_method', 'payment_status', 'transaction_id')
    list_filter = ('payment_status', 'payment_method', 'payment_date')
    search_fields = ('transaction_id', 'booking__customer__first_name')
    readonly_fields = ('payment_date',)
    list_per_page = 20
    fieldsets = (
        ('Payment Details', {
            'fields': ('booking', 'amount', 'payment_method', 'payment_status')
        }),
        ('Transaction Information', {
            'fields': ('transaction_id', 'payment_proof')
        }),
        ('Refund', {
            'fields': ('refund_status',)
        })
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'travel_package', 'rating', 'review_date', 'is_verified', 'likes')
    list_filter = ('rating', 'review_date', 'is_verified')
    search_fields = ('user__username', 'travel_package__name', 'comment')
    list_editable = ('is_verified',)
    readonly_fields = ('review_date', 'reply_date', 'likes')
    list_per_page = 20
    fieldsets = (
        ('Review Details', {
            'fields': ('user', 'travel_package', 'rating', 'comment', 'images')
        }),
        ('Response', {
            'fields': ('reply', 'reply_date')
        }),
        ('Metrics', {
            'fields': ('likes', 'is_verified')
        })
    )


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('hotels', 'activities', 'packages')
    search_fields = ('user__username', 'user__email')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name',  'best_time_to_visit', 'climate')
    search_fields = ('name', 'best_time_to_visit')
    list_filter = ('best_time_to_visit', 'climate')
    list_per_page = 20
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description',  'image')
        }),
        ('Additional Details', {
            'fields': ('best_time_to_visit', 'climate', 'popular_attractions')
        }),
        ('Related Content', {
            'fields': ('hotels', 'activities', 'travel_packages')
        }),
    )
    filter_horizontal = ('hotels', 'activities', 'travel_packages')
