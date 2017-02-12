# coding=utf-8

from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch.dispatcher import receiver
from django.utils.text import slugify
from django_resized import ResizedImageField
from tinymce.models import HTMLField
import tweepy
from phonenumber_field.modelfields import PhoneNumberField

# Over-ride default string representation of a user.
def user_unicode(self):
    return  u'%s %s (%s)' % (self.first_name.title(), self.last_name.title(), self.username)
User.__unicode__ = user_unicode

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.user.username, filename)

class Document(models.Model):
    user = models.ForeignKey(User)
    document = models.ImageField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)



class Profile(models.Model):
    
    # Driving licence shorts

    drivinglicence = 'DL'
    passport = 'PP'
    nationalID = 'NI'
    
    # House occupancey shorts
    
    overtwoyears = 'O2'
    undertwoyears = 'U2'
    
    
    
    id_choices = (
                              (drivinglicence, 'Driving Licence'),
                              (passport, 'Passport'),
                              (nationalID, 'Mational ID'),
                              )
    house_occupancy_choices = (
                  (overtwoyears, 'Over 2 Years'),
                  (undertwoyears, 'Under 2 Years'),
                  )
                  
                  
    user = models.OneToOneField(User, unique = False)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    referral_code = models.PositiveSmallIntegerField()
    add1housenumberorname = models.CharField(max_length=30, null=True, blank=True)
    add1street1 = models.CharField(max_length=30, null=True, blank=True)
    add1street2 = models.CharField(max_length=30, null=True, blank=True)
    add1townorcity = models.CharField(max_length=30, null=True, blank=True)
    add1county = models.CharField(max_length=30, null=True, blank=True)
    add1country = models.CharField(max_length=30, null=True, blank=True)
    add1postcode = models.CharField(max_length=10, null=True, blank=True)
    add2housenumberorname = models.CharField(max_length=30, null=True, blank=True)
    add2street1 = models.CharField(max_length=30, null=True, blank=True)
    add2street2 = models.CharField(max_length=30, null=True, blank=True)
    add2townorcity = models.CharField(max_length=30, null=True, blank=True)
    add2county = models.CharField(max_length=30, null=True, blank=True)
    add2country = models.CharField(max_length=30, null=True, blank=True)
    add2postcode = models.CharField(max_length=10, null=True, blank=True)
    id_choice = models.CharField(
                                 max_length=2,
                                 choices=id_choices,
                                 )
    house_occupancy_choice = models.CharField(
                                              max_length=2,
                                              choices=house_occupancy_choices,
                                              )

    class Meta:
        managed = True
        db_table = 'fbf_profile'


