import datetime
from unicodedata import name
from django.db import models
from django.conf import settings
from django_countries.fields import *
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from pytz import timezone # new



#from django.contrib.localflavor.pt.models import USStateField

# Create your models here.

class Customer(models.Model):
	GENDER_MALE = 0
	GENDER_FEMALE = 1
	GENDER_OTHER = 3
	GENDER_COMPANY = 4
	GENDER_CHOICES = [
		(GENDER_COMPANY, 'Empresa'),
		(GENDER_MALE, 'Masculino'), 
		(GENDER_FEMALE, 'Feminino'),
		(GENDER_OTHER, 'Outro')
		]		
	title = models.ForeignKey("Title", null=True, on_delete=models.SET_NULL, default=1)
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

class Employee(models.Model):
	GENDER_MALE = 0
	GENDER_FEMALE = 1
	GENDER_OTHER = 3
	GENDER_COMPANY = 4
	GENDER_CHOICES = [
		(GENDER_COMPANY, 'Empresa'),
		(GENDER_MALE, 'Masculino'), 
		(GENDER_FEMALE, 'Feminino'),
		(GENDER_OTHER, 'Outro')
		]		
	title = models.ForeignKey("Title", null=True, on_delete=models.SET_NULL, default=1)
	gender = models.IntegerField(choices=GENDER_CHOICES, default=0)
	name = models.CharField(max_length=200, blank=False, unique=False)
	address = models.TextField(null=True, blank=True)
	zipCode =  models.CharField(max_length=8, null=True, blank=True)
	city = models.CharField(max_length=200, null=True, blank=True)
	country = CountryField(null=True, blank=True)
	taxNumber = models.CharField(max_length=12, blank=True, null=True)
	dateOfBirth = models.DateField(blank=True, null=True)
	phone = PhoneNumberField(blank=True, null=True)
	contactByEmail = models.BooleanField(blank=False, null=False, default=False)
	contactBySMS = models.BooleanField(blank=False, null=False, default=False)
	contactByPhone = models.BooleanField(blank=False, null=False, default=False)

class Invoice(models.Model):
	customer = models.ForeignKey("Customer",null=False, blank=False, on_delete=models.CASCADE)
	date = models.DateTimeField(blank=False, null=False)
	employee = models.ForeignKey("Employee",null=True, blank=True, on_delete=models.CASCADE)

class InvoiceItem(models.Model):
	invoice = models.ForeignKey("Invoice",null=False, blank=False, on_delete=models.CASCADE)
	output = models.ForeignKey("ItemOutput",null=False, blank=False, on_delete=models.CASCADE)

class Item(models.Model):
	CATEGORY_PRODUCT = 0
	CATEGORY_SERVICE = 1
	CATEGORY_CHOICES = [
		(CATEGORY_PRODUCT, 'Produto'),
		(CATEGORY_SERVICE, 'Serviço')
		]
	category = models.IntegerField(choices=CATEGORY_CHOICES, default=0)
	iva = models.ForeignKey("Iva",null=True, blank=False, on_delete=models.SET_NULL)
	unit = models.ForeignKey("Unit",null=True, blank=False, on_delete=models.SET_NULL)
	cost = models.FloatField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	external_Ref = models.CharField(max_length=12, blank=True, null=True)
	weight = models.FloatField(null=True, blank=True)
	origin = CountryField(null=True, blank=True)
	notes = models.TextField(null=True, blank=True)
	supplier_Id = models.ForeignKey("Supplier", null=True, blank=False, on_delete=models.SET_NULL)
	pvp = models.FloatField(null=True, blank=True)

class ItemInput(models.Model):
	item = models.ForeignKey("Item", null=False, blank=False, on_delete=models.CASCADE)
	warehouse = models.ForeignKey("Warehouse", null=True, on_delete=models.CASCADE)
	iva = models.ForeignKey("Iva",null=False, blank=False, on_delete=models.CASCADE)
	cost = models.FloatField(null=False, blank=False)
	quantity = models.IntegerField(null=False, blank=False)

class ItemOutput(models.Model):
	item = models.ForeignKey("Item", null=False, blank=False, on_delete=models.CASCADE)
	warehouse = models.ForeignKey("Warehouse", null=True, on_delete=models.CASCADE)
	iva = models.ForeignKey("Iva",null=True, blank=False, on_delete=models.CASCADE)
	cost = models.FloatField(null=True, blank=True)
	quantity = models.IntegerField(null=True, blank=True)
	input = models.ForeignKey("ItemInput",null=False, blank=False, on_delete=models.CASCADE)

class Iva(models.Model):
	rate = models.IntegerField(null=False, blank=False)
	name = models.CharField(max_length=200, blank=False, unique=True)

	def __str__(self):
		return self.name + " (" + str(self.rate) + "%)"

class Position(models.Model):
	name = models.CharField(max_length=200, blank=False, unique=False)
	description = models.TextField(null=True, blank=True)

class Warehouse(models.Model):
	name = models.CharField(max_length=200, blank=False, unique=False)
	description = models.TextField(null=True, blank=True)
	address = models.TextField(null=True, blank=True)

class Store(Warehouse):
    pass

class External_Warehouse(Warehouse):
	pass

class Movement(models.Model):
	product_Id = models.ForeignKey(Item, null=True, blank=False, on_delete=models.SET_NULL)
	quantity = models.FloatField(null=False, blank=False)
	source = models.ForeignKey(External_Warehouse, null=True, on_delete=models.SET_NULL)
	destination = models.ForeignKey(Store, null=True, on_delete=models.SET_NULL)
	cost = models.FloatField(null=False, blank=False)
	document_Id = models.TextField(null=False, blank=False)
	input = models.ForeignKey(ItemInput, null=True, blank=True, on_delete=models.SET_NULL)
	output = models.ForeignKey(ItemOutput, null=True, blank=True, on_delete=models.SET_NULL)


class Supplier(models.Model):
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

	def __str__(self):
		return self.name

class Task(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=500, null=True, blank=True)
	startDate = models.DateField(null=True, blank=True)
	endDate = models.DateField(null=True, blank=True)
	startTime = models.TimeField(null=True, blank=True)
	endTime = models.TimeField(null=True, blank=True)
	createdOn = models.DateTimeField(editable=False, auto_now_add=True)
	updatedOn = models.DateTimeField(auto_now=True)
	createdBy = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="created_by_user_profile",
		default=1,
	)
	assignedTo = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="assigned_to_user_profile",
		default=1,
	)
	completed = models.BooleanField(default=False)

	def __str__(self):
		return self.title
	
class Title(models.Model):
	title = models.CharField(max_length=10)
	
	def __str__(self):
		return self.title

class Unit(models.Model):
	name = models.CharField(max_length=10)
	description = models.CharField(max_length=100)

	def __str__(self):
		return self.name

