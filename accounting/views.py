from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import ObjectDoesNotExist
from django.core.paginator import Paginator #import Paginator
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

@login_required
def index(request):
	return html(request, "index")


def html(request, filename):
	context = {"filename": filename, "collapse": ""}
	
	if request.user.is_anonymous and filename != "login":
		return redirect("/login.html")
		
	if filename == "logout":
		logout(request)
		return redirect("/")
		
	if filename == "login" and request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		try:
			if "@" in username:
				user = User.objects.get(email=username)
			else:
				user = User.objects.get(username=username)
			user = authenticate(request, username=user.username, password=password)
			if user is not None:
				login(request, user)
				return redirect("/")
			else:
				context["error"] = "Wrong password"
		except ObjectDoesNotExist:
			context["error"] = "User not found"
			
		print("login")
		print(username, password)
	print(filename, request.method)
	if filename in ["buttons", "cards"]:
		context["collapse"] = "components"

	if filename in ["utilities-color", "utilities-border", "utilities-animation", "utilities-other"]:
		context["collapse"] = "utilities"

	if filename in ["404", "blank"]:
		context["collapse"] = "pages"
		
	return render(request, f"{filename}.html", context=context)


@login_required
def costumerList_view(request):
	
	costumers = Costumer.objects.all()
	context = {
		'costumers': costumers,
		'collapse': 'Sales'
	}

	return render(request=request, template_name="CostumerList.html", context=context)


@login_required
def costumerNew_view(request):
    # create object of form
	form = CostumerForm(request.POST or None, request.FILES or None)
	
	if form.is_valid():
		form.save()
		return redirect("/costumers/")	

	context = {
		'form': form,
		'collapse': 'Sales'
	}

	return render(request, 'CostumerNew.html', context=context)

@login_required
def titleList_view(request):

	titles = Title.objects.all() 
	context = {
		'titles': titles,
		'collapse': 'Settings'
	}
	return render(request=request, template_name="TitleList.html", context=context)

@login_required
def titleNew_view(request):

	form = TitleForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		return redirect("/titles/")	

	context = {
		'form': form,
		'collapse': 'Settings'
	}

	return render(request, 'TitleNew.html', context=context)


@login_required
def TitleBulkAction_view(request, id=None):	

	if request.method == 'POST':
		id_list = request.POST.getlist('instance')
		# This will submit an array of the value attributes of all the
		# checkboxes that have been checked, that is an array of {{obj.id}}

		# Now all that is left is to iterate over the array fetch the   
		# object with the ID and delete it. 
		for title_id in id_list:
			Title.objects.get(id=title_id).delete()
		# maybe in some other cases it is not possible to delete an object
		# as it may be foreigh key to another object
		# in those cases it is better to issue a warning message

	return redirect('titleList')	