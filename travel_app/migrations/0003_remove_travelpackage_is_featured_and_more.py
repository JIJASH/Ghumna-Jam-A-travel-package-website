# Generated by Django 5.1.5 on 2025-01-24 17:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app', '0002_activity_booking_cancellation_reason_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelpackage',
            name='is_featured',
        ),
        migrations.AlterField(
            model_name='activity',
            name='equipment_provided',
            field=models.JSONField(default=list, help_text='Example: ["helmet", "harness", "ropes"]'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='emergency_contact',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='rating',
            field=models.FloatField(blank=True, help_text='Hotel rating from 1.0 to 5.0 stars', null=True, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='website',
            field=models.URLField(blank=True, help_text="The hotel's website URL : https://www.hotelwebsite.com", null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('ESEWA', 'ESEWA'), ('Credit Card', 'Credit Card')], max_length=20),
        ),
        migrations.AlterField(
            model_name='tourguide',
            name='certification',
            field=models.FileField(blank=True, null=True, upload_to='guide_certifications/'),
        ),
    ]
