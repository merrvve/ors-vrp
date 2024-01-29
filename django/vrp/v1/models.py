from django.db import models
from datetime import date, datetime
from pytz import timezone
from django_jsonform.models.fields import ArrayField
ist= timezone('Europe/Istanbul')

class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    skills = models.ManyToManyField(Skill)
    capacity = ArrayField(models.IntegerField())
    end = ArrayField(models.FloatField(), size=2, default=list)  
    start = ArrayField(models.FloatField(), size=2, default=list)  
    time_window = ArrayField(models.IntegerField(), size=2,  default=list)

    def __str__(self):
        return f"Vehicle {self.id}"




class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = ArrayField(models.FloatField(), size=2)
    def __str__(self):
        return f"Warehuse {self.name} {self.id}"
	

class Route(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    job_date = models.DateField()
    steps = ArrayField(ArrayField(models.FloatField(), size=2))
    googlelink=models.TextField(max_length=2048, default='',blank=True)
    fulfillment_ids=ArrayField(models.CharField(max_length=36),default=list)

    def __str__(self):
        return f"Route for {self.vehicle} on {self.job_date}"


class Destination(models.Model):
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    company = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    province = models.CharField(max_length=100)
    zip = models.CharField(max_length=20)
    latitude = models.DecimalField(blank=True,max_digits=20,decimal_places=15)
    longitude = models.DecimalField(blank=True,max_digits=20,decimal_places=15)

class FulfillmentLineItem(models.Model):
    line_item_id = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255)
    quantity = models.IntegerField()
    delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(blank=True)

class Fulfillment(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    channel_id = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True)
    delivered_at = models.DateTimeField(blank=True)
    display_status = models.CharField(max_length=255,blank=True)
    in_transit_at = models.DateTimeField(blank=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255,blank=True)
    shipment_status = models.CharField(max_length=255,blank=True)
    total_quantity = models.IntegerField()
    fulfillment_tracking_company = models.CharField(max_length=255)
    fulfillment_tracking_numbers = models.CharField(max_length=255)
    fulfillment_tracking_urls = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    email_notification = models.BooleanField(default=False)
    sms_notification = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    fulfillment_line_items = models.ManyToManyField(FulfillmentLineItem)

