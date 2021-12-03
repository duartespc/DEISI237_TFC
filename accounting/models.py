from django.db import models
from django_countries.fields import *
from phonenumber_field.modelfields import PhoneNumberField

#from django.contrib.localflavor.pt.models import USStateField

# Create your models here.


class Title(models.Model):
	title = models.CharField(max_length=10)
	def __str__(self):
		return self.title

class Costumer(models.Model):
	GENDER_MALE = 0
	GENDER_FEMALE = 1
	GENDER_OTHER = 3
	GENDER_COMPANY = 4
	GENDER_CHOICES = [
		(GENDER_COMPANY, 'Company'),
		(GENDER_MALE, 'Male'), 
		(GENDER_FEMALE, 'Female'),
		(GENDER_OTHER, 'Other')
		]		
	title = models.ForeignKey(Title, null=True, on_delete=models.SET_NULL, default=1)
	gender = models.IntegerField(choices=GENDER_CHOICES, default=0)
	name = models.CharField(max_length=200, blank=False, unique=False)
	address = models.TextField(null=True, blank=True)
	zipCode =  models.CharField(max_length=8, null=True, blank=True)
	city = models.CharField(max_length=200, null=True, blank=True)
	country = CountryField(null=True, blank=True)
	website = models.URLField(max_length=200, blank=True, null=True)
	taxNumber = models.CharField(max_length=12, blank=True, null=True)
	dateOfBirth = models.DateField(blank=True, null=True)
	phone = PhoneNumberField(blank=True, null=True)
	contactByEmail = models.BooleanField(blank=False, null=False, default=False)
	contactBySMS = models.BooleanField(blank=False, null=False, default=False)
	contactByPhone = models.BooleanField(blank=False, null=False, default=False)



	    
