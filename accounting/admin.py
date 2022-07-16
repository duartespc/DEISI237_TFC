import unittest
from django.contrib import admin
from .models import Task, Event, ItemInput

# Register your models here.

admin.site.register(Task)
admin.site.register(Event)
admin.site.register(ItemInput)
