from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=20, null=True, blank=True)
    bio = models.CharField(max_length=50, null=True, blank=True)
    phonenumber = models.CharField(max_length=10, null=True, blank=True)
    interest = models.CharField(max_length=50, null=True, blank=True)
    documents = models.TextField(null=True, blank=True) # document path
    birth_date = models.DateField(null = True, blank=False)
    home_location = models.CharField(max_length=30, blank=False)
    office_location = models.CharField(max_length=30, blank=False)
    
class Home(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

class Office(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

class Line(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    line_vector = models.CharField(max_length=500, null=True, blank=True)
    # blob or array is not supported in sqlite

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()