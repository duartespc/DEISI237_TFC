from django import forms
from .models import *


class CostumerForm(forms.ModelForm):
	class Meta:
		model = Costumer
		fields = "__all__"

class TitleForm(forms.ModelForm):
	class Meta:
		model = Title
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super(TitleForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
		})