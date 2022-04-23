from django import forms
import datetime


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class TimePickerInput(forms.TimeInput):
    input_type = 'time'
