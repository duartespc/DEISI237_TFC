import datetime
from unicodedata import name
from django.db import models
from django.conf import settings
from django.forms import DateTimeField
from django_countries.fields import *
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _  # use if you support internationalization

#from django.contrib.localflavor.pt.models import USStateField

# Create your models here.


def validate_interval(value):
    if value < 0.0 or value > 100.0:
        raise ValidationError(
            _('%(value)s must be in the range [0.0, 100.0]'),
            params={'value': value},
        )


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField(default=datetime.date.today)
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id, ))
        return f'<a href="{url}"> {self.title} </a>'


class Saft(models.Model):

    def save(self, *args, **kwargs):
        self.full_clean()  # or clean
        super().save(*args, **kwargs)

    MONTH_NONE = 0
    MONTH_JANUARY = 1
    MONTH_FEBRUARY = 2
    MONTH_MARCH = 3
    MONTH_APRIL = 4
    MONTH_MAY = 5
    MONTH_JUNE = 6
    MONTH_JULY = 7
    MONTH_AUGUST = 8
    MONTH_SEPTEMBER = 9
    MONTH_OCTOBER = 10
    MONTH_NOVEMBER = 11
    MONTH_DECEMBER = 12
    MONTH_CHOICES = [(MONTH_JANUARY, 'Janeiro'), (MONTH_FEBRUARY, 'Fevereiro'),
                     (MONTH_MARCH, 'Março'), (MONTH_APRIL, 'Abril'),
                     (MONTH_MAY, 'Maio'), (MONTH_JUNE, 'Junho'),
                     (MONTH_JULY, 'Julho'), (MONTH_AUGUST, 'Agosto'),
                     (MONTH_SEPTEMBER, 'Setembro'), (MONTH_OCTOBER, 'Outubro'),
                     (MONTH_NOVEMBER, 'Novembro'),
                     (MONTH_DECEMBER, 'Dezembro')]
    zeroStock = models.BooleanField(null=False, blank=False)
    itemProfitRate = models.FloatField(null=False,
                                       blank=False,
                                       validators=[validate_interval])
    month = models.IntegerField(choices=MONTH_CHOICES, default=0)
    file = models.FileField(null=False, blank=False)


class Customer(models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_OTHER = 3
    GENDER_COMPANY = 4
    GENDER_CHOICES = [(GENDER_COMPANY, 'Empresa'), (GENDER_MALE, 'Masculino'),
                      (GENDER_FEMALE, 'Feminino'), (GENDER_OTHER, 'Outro')]
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0)
    name = models.CharField(max_length=100, blank=False, unique=False)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    zipCode = models.CharField(max_length=8, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    website = models.URLField(max_length=100, blank=True, null=True)
    taxNumber = models.CharField(max_length=9, blank=True, null=True)
    dateOfBirth = models.DateField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    contactByEmail = models.BooleanField(blank=False,
                                         null=False,
                                         default=True)
    contactBySMS = models.BooleanField(blank=False, null=False, default=False)
    contactByPhone = models.BooleanField(blank=False,
                                         null=False,
                                         default=False)

    def __str__(self):
        return self.name


class Email(models.Model):
    author = models.ForeignKey(User,
                               null=False,
                               blank=False,
                               on_delete=models.CASCADE,
                               related_name="author")
    subject = models.TextField(null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(editable=False, auto_now_add=True)


class Employee(models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_OTHER = 3
    GENDER_COMPANY = 4
    GENDER_CHOICES = [(GENDER_COMPANY, 'Empresa'), (GENDER_MALE, 'Masculino'),
                      (GENDER_FEMALE, 'Feminino'), (GENDER_OTHER, 'Outro')]
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0)
    name = models.CharField(max_length=200, blank=False, unique=False)
    address = models.TextField(null=True, blank=True)
    zipCode = models.CharField(max_length=8, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    taxNumber = models.CharField(max_length=12, blank=True, null=True)
    dateOfBirth = models.DateField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    contactByEmail = models.BooleanField(blank=False,
                                         null=False,
                                         default=False)
    contactBySMS = models.BooleanField(blank=False, null=False, default=False)
    contactByPhone = models.BooleanField(blank=False,
                                         null=False,
                                         default=False)

    def __str__(self):
        return self.name


class Payment(models.Model):
    description = models.TextField(null=False, blank=False)
    cost = models.FloatField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    employee = models.ForeignKey("Employee",
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL)


class Invoice(models.Model):
    #InvoiceType - Invoice or Invoice Receipt -- TODO
    #  ?????? storage ??? - is it warehouse?
    docNumber = models.CharField(max_length=20,
                                 unique=True,
                                 null=False,
                                 blank=False)
    customer = models.ForeignKey("Customer",
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL)
    date = models.DateTimeField(blank=False, null=False)
    tax = models.FloatField(null=True, blank=True)
    netTotal = models.FloatField(null=True, blank=True)
    grossTotal = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.docnumber


class InvoiceItem(models.Model):
    invoice = models.ForeignKey("Invoice",
                                null=False,
                                blank=False,
                                on_delete=models.CASCADE)
    output = models.ForeignKey("ItemOutput",
                               null=False,
                               blank=False,
                               on_delete=models.CASCADE)


class Item(models.Model):
    CATEGORY_PRODUCT = 0
    CATEGORY_SERVICE = 1
    CATEGORY_CHOICES = [(CATEGORY_PRODUCT, 'Produto'),
                        (CATEGORY_SERVICE, 'Serviço')]
    code = models.CharField(max_length=15,
                            unique=True,
                            null=False,
                            blank=False)
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=0)
    tax = models.FloatField(null=False, blank=False)
    cost = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    external_Ref = models.CharField(max_length=12, blank=True, null=True)
    weight = models.FloatField(null=True, blank=True)
    origin = CountryField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    supplier_Id = models.ForeignKey("Supplier",
                                    null=True,
                                    blank=False,
                                    on_delete=models.SET_NULL)
    pvp = models.FloatField(null=True, blank=True)
    quantity_In_Stock = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.code


class ItemInput(models.Model):
    date = models.DateTimeField(blank=False, null=False)
    item = models.ForeignKey("Item",
                             null=False,
                             blank=False,
                             on_delete=models.CASCADE)
    #warehouse = models.ForeignKey("Warehouse", null=True, on_delete=models.CASCADE)
    tax = models.FloatField(null=False, blank=False)
    cost = models.FloatField(null=False, blank=False)
    quantity = models.FloatField(null=False, blank=False)
    total = models.FloatField(null=True, blank=True)
    #discount = models.FloatField(null=False, blank=False)
    order = models.ForeignKey("Order",
                              null=True,
                              blank=True,
                              on_delete=models.CASCADE)


class ItemOutput(models.Model):
    date = models.DateTimeField(blank=False, null=False)
    item = models.ForeignKey("Item",
                             null=False,
                             blank=False,
                             on_delete=models.CASCADE)
    #warehouse = models.ForeignKey("Warehouse", null=True, on_delete=models.CASCADE)
    tax = models.FloatField(null=False, blank=False)
    cost = models.FloatField(null=False, blank=False)
    quantity = models.FloatField(null=False, blank=False)
    total = models.FloatField(null=False, blank=False)
    #discount = models.FloatField(null=True, blank=True)


class Position(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=False)
    description = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Store(Warehouse):
    pass


class External_Warehouse(Warehouse):
    pass


class Message(models.Model):
    sender = models.ForeignKey(User,
                               null=False,
                               blank=False,
                               on_delete=models.CASCADE,
                               related_name="sender")
    receiver = models.ForeignKey(User,
                                 null=False,
                                 blank=False,
                                 on_delete=models.CASCADE,
                                 related_name="receiver")
    msg_content = models.TextField(null=False, blank=False)
    created_At = models.DateTimeField(editable=False, auto_now_add=True)


class Movement(models.Model):
    product_Id = models.ForeignKey(Item,
                                   null=True,
                                   blank=False,
                                   on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=False, blank=False)
    source = models.ForeignKey(External_Warehouse,
                               null=True,
                               on_delete=models.SET_NULL)
    destination = models.ForeignKey(Store,
                                    null=True,
                                    on_delete=models.SET_NULL)
    cost = models.FloatField(null=False, blank=False)
    document_Id = models.TextField(null=False, blank=False)
    input = models.ForeignKey(ItemInput,
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL)
    output = models.ForeignKey(ItemOutput,
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)


class Order(models.Model):
    item = models.ForeignKey("Item",
                             null=True,
                             blank=False,
                             on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=False, blank=False)
    cost = models.FloatField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    tax = models.FloatField(null=False, blank=False)
    supplier = models.ForeignKey("Supplier",
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL)
    warehouse = models.ForeignKey("Warehouse",
                                  null=True,
                                  blank=True,
                                  on_delete=models.SET_NULL)
    description = models.TextField(null=False, blank=True)

    def __str__(self):
        return self.item.code


class Supplier(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=False)
    address = models.TextField(null=True, blank=True)
    zipCode = models.CharField(max_length=8, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    taxNumber = models.CharField(max_length=12, blank=True, null=True)
    dateOfBirth = models.DateField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    contactByEmail = models.BooleanField(blank=False,
                                         null=False,
                                         default=False)
    contactBySMS = models.BooleanField(blank=False, null=False, default=False)
    contactByPhone = models.BooleanField(blank=False,
                                         null=False,
                                         default=False)

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
