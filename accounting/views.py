from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from turtle import pd
from typing_extensions import Required
from django.forms import modelform_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import ObjectDoesNotExist
from django.core.paginator import Paginator  #import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime as dt
import pdb

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
            user = authenticate(request,
                                username=user.username,
                                password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                context["error"] = "Palavra-passe errada"
        except ObjectDoesNotExist:
            context["error"] = "Utilizador não encontrado"

        print("login")
        print(username, password)
    print(filename, request.method)
    if filename in ["buttons", "cards"]:
        context["collapse"] = "components"

    if filename in [
            "utilities-color", "utilities-border", "utilities-animation",
            "utilities-other"
    ]:
        context["collapse"] = "utilities"

    if filename in ["404", "blank"]:
        context["collapse"] = "pages"

    return render(request, f"{filename}.html", context=context)


@login_required
@permission_required('accounting.view_customer')
def CustomerList_view(request):
    current_user = request.user
    form = CustomerForm(request.POST or None, request.FILES or None)
    if form.is_valid() and current_user.has_perm('accounting.add_customer'):
        form.save()
        return redirect('CustomerList')
    customers = Customer.objects.all()
    context = {'form': form, 'customers': customers, 'collapse': 'Sales'}
    return render(request=request,
                  template_name="customerList.html",
                  context=context)

@login_required
@permission_required('accounting.view_employee')
def EmployeeList_view(request):
    current_user = request.user
    form = EmployeeForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_employee'):
        form.save()
        return redirect('EmployeeList')
    employees = Employee.objects.all()
    context = {'form': form, 'employees': employees, 'collapse': 'HR'}

    return render(request=request,
                  template_name="employeeList.html",
                  context=context)


@login_required
@permission_required('accounting.view_item')
def ItemList_view(request):
    current_user = request.user
    form = ItemForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_item'):
        form.save()
        return redirect('ItemList')

    items = Item.objects.all()
    context = {'form': form, 'items': items, 'collapse': 'Items'}

    return render(request=request,
                  template_name="itemList.html",
                  context=context)


@login_required
@permission_required('accounting.view_item')
def InventoryList_view(request):
    current_user = request.user
    items = Item.objects.all()
    context = {'items': items, 'collapse': 'Items'}

    return render(request=request,
                  template_name="inventoryList.html",
                  context=context)


@login_required
@permission_required('accounting.view_invoice')
def InvoiceList_view(request):
    current_user = request.user
    context = {'collapse': 'Customers'}

    return render(request=request,
                  template_name="invoiceList.html",
                  context=context)


@login_required
@permission_required('accounting.view_iva')
def IvaList_view(request):
    current_user = request.user
    form = IvaForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_iva'):
        form.save()
        return redirect('IvaList')

    ivas = Iva.objects.all()
    context = {'form': form, 'ivas': ivas, 'collapse': 'Settings'}
    return render(request=request,
                  template_name="ivaList.html",
                  context=context)


@login_required
@permission_required('accounting.view_payment')
def PaymentList_view(request):
    current_user = request.user
    context = {'collapse': 'Customers'}

    return render(request=request,
                  template_name="paymentList.html",
                  context=context)


@login_required
@permission_required('accounting.view_position')
def PositionList_view(request):
    current_user = request.user
    form = PositionForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_position'):
        form.save()
        return redirect('PositionList')

    positions = Position.objects.all()
    context = {'form': form, 'positions': positions, 'collapse': 'HR'}

    return render(request=request,
                  template_name="positionList.html",
                  context=context)


@login_required
@permission_required('accounting.view_task')
def TaskList_view(request):
    current_user = request.user
    form = TaskForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_task'):
        post = form.save(commit=False)
        post.createdBy = request.user
        post.updatedOn = dt.now()
        post.save()
        return redirect('TaskList')

    tasks = Task.objects.all()
    context = {
        'tasks': tasks,
    }

    return render(request=request,
                  template_name="taskList.html",
                  context=context)

@login_required
@permission_required('accounting.view_title')
def TitleList_view(request):
    current_user = request.user
    form = TitleForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_title'):
        form.save()
        return redirect('TitleList')

    titles = Title.objects.all()
    context = {'form': form, 'titles': titles, 'collapse': 'Settings'}
    return render(request=request,
                  template_name="titleList.html",
                  context=context)


@login_required
@permission_required('accounting.view_warehouse')
def WarehouseList_view(request):
    current_user = request.user
    form = WarehouseForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_warehouse'):
        form.save()
        return redirect('WarehouseList')

    warehouses = Warehouse.objects.all()
    context = {'form': form, 'warehouses': warehouses, 'collapse': 'Items'}

    return render(request=request,
                  template_name="warehouseList.html",
                  context=context)


@login_required
@permission_required('accounting.view_supplier')
def SupplierList_view(request):
    current_user = request.user
    form = SupplierForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_supplier'):
        form.save()
        return redirect('SupplierList')

    suppliers = Supplier.objects.all()
    context = {'form': form, 'suppliers': suppliers, 'collapse': 'Customers'}

    return render(request=request,
                  template_name="supplierList.html",
                  context=context)

@login_required
def UserInfo_view(request):
    current_user = request.user
    context = {'user': current_user}
    return render(request=request, template_name="userInfo.html", context=context)

@login_required
def CustomerEdit_view(request, customer_id):
    current_user = request.user
    # Edit object of form
    customer = Customer.objects.get(id=customer_id)

    form = CustomerForm(request.POST or None, instance=customer)

    if request.POST and form.is_valid() and current_user.has_perm('accounting.edit_customer'):
        form.save()
        return redirect('CustomerList')

    context = {'form': form, 'customer': customer, 'collapse': 'Sales'}

    return render(request, 'customerEdit.html', context=context)

@login_required
def EmployeeEdit_view(request, employee_id):
    current_user = request.user
    # Edit object of form
    employee = Employee.objects.get(id=employee_id)

    form = EmployeeForm(request.POST or None, instance=employee)

    if request.POST and form.is_valid() and current_user.has_perm('accounting.edit_employee'):
        form.save()
        return redirect('EmployeeList')

    context = {'form': form, 'employee': employee, 'collapse': 'HR'}

    return render(request, 'employeeEdit.html', context=context)


@login_required
def ItemEdit_view(request, item_id):
    current_user = request.user
    # Edit object of form
    item = Item.objects.get(id=item_id)

    form = ItemForm(request.POST or None, instance=item)

    if request.POST and form.is_valid() and current_user.has_perm('accounting.edit_item'):
        form.save()
        return redirect('ItemList')

    context = {'form': form, 'item': item, 'collapse': 'Items'}

    return render(request, 'itemEdit.html', context=context)

@login_required
def IvaEdit_view(request, iva_id):
    current_user = request.user
    # Edit object of form
    iva = Iva.objects.get(id=iva_id)

    form = IvaForm(request.POST or None, instance=iva)

    if request.POST and form.is_valid() and current_user.has_perm('accounting.edit_iva'):
        form.save()
        return redirect('IvaList')

    context = {'form': form, 'iva': iva, 'collapse': 'Settings'}

    return render(request, 'ivaEdit.html', context=context)


@login_required
def PositionEdit_view(request, position_id):
    current_user = request.user
    # Edit object of form
    position = Position.objects.get(id=position_id)

    form = PositionForm(request.POST or None, instance=position)

    if request.POST and form.is_valid() and current_user.has_perm('accounting.edit_position'):
        form.save()
        return redirect('PositionList')

    context = {'form': form, 'position': position, 'collapse': 'HR'}

    return render(request, 'positionEdit.html', context=context)


@login_required
def SupplierEdit_view(request, supplier_id):
    current_user = request.user
    # Edit object of form
    supplier = Supplier.objects.get(id=supplier_id)

    form = SupplierForm(request.POST or None, instance=supplier)

    if request.POST and form.is_valid() and current_user.has_perm('accounting.edit_supplier'):
        form.save()
        return redirect('SupplierList')

    context = {'form': form, 'supplier': supplier, 'collapse': 'Purchases'}

    return render(request, 'supplierEdit.html', context=context)


@login_required
def TaskEdit_view(request, task_id):
    current_user = request.user
    # Edit object of form
    task = Task.objects.get(id=task_id)

    form = TaskForm(request.POST or None, instance=task)

    if request.POST and form.is_valid() and current_user.has_perm('accounting.edit_task'):
        form.save()
        return redirect('TaskList')

    context = {'form': form, 'task': task}

    return render(request, 'taskEdit.html', context=context)


@login_required
def TitleEdit_view(request, title_id):
    current_user = request.user
    # Edit object of form
    title = Title.objects.get(id=title_id)

    form = TitleForm(request.POST or None, instance=title)

    if request.POST and form.is_valid() and current_user.has_perm('accounting.edit_title'):
        form.save()
        return redirect('TitleList')

    context = {'form': form, 'title': title, 'collapse': 'Settings'}

    return render(request, 'titleEdit.html', context=context)


@login_required
def WarehouseEdit_view(request, warehouse_id):
    current_user = request.user
    # Edit object of form
    warehouse = Warehouse.objects.get(id=warehouse_id)

    form = WarehouseForm(request.POST or None, instance=warehouse)

    if request.POST and form.is_valid() and current_user.has_perm('accounting.edit_warehouse'):
        form.save()
        return redirect('WarehouseList')

    context = {'form': form, 'warehouse': warehouse, 'collapse': 'Items'}

    return render(request, 'warehouseEdit.html', context=context)

@login_required
def CustomerBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm('accounting.delete_customer'):
        id_list = request.POST.getlist('instance')
        # This will submit an array of the value attributes of all the
        # checkboxes that have been checked, that is an array of {{obj.id}}

        # Now all that is left is to iterate over the array fetch the
        # object with the ID and delete it.
        for customer_id in id_list:
            Customer.objects.get(id=customer_id).delete()
        # maybe in some other cases it is not possible to delete an object
        # as it may be foreigh key to another object
        # in those cases it is better to issue a warning message

    return redirect('CustomerList')


@login_required
def EmployeeBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm('accounting.delete_employee'):
        id_list = request.POST.getlist('instance')
        # This will submit an array of the value attributes of all the
        # checkboxes that have been checked, that is an array of {{obj.id}}

        # Now all that is left is to iterate over the array fetch the
        # object with the ID and delete it.
        for employee_id in id_list:
            Employee.objects.get(id=employee_id).delete()
        # maybe in some other cases it is not possible to delete an object
        # as it may be foreigh key to another object
        # in those cases it is better to issue a warning message

    return redirect('EmployeeList')


@login_required
def ItemBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm('accounting.delete_item'):
        id_list = request.POST.getlist('instance')
        # This will submit an array of the value attributes of all the
        # checkboxes that have been checked, that is an array of {{obj.id}}

        # Now all that is left is to iterate over the array fetch the
        # object with the ID and delete it.
        for item_id in id_list:
            Item.objects.get(id=item_id).delete()
        # maybe in some other cases it is not possible to delete an object
        # as it may be foreigh key to another object
        # in those cases it is better to issue a warning message

    return redirect('ItemList')


@login_required
def IvaBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm('accounting.delete_iva'):
        id_list = request.POST.getlist('instance')
        # This will submit an array of the value attributes of all the
        # checkboxes that have been checked, that is an array of {{obj.id}}

        # Now all that is left is to iterate over the array fetch the
        # object with the ID and delete it.
        for iva_id in id_list:
            Iva.objects.get(id=iva_id).delete()
        # maybe in some other cases it is not possible to delete an object
        # as it may be foreigh key to another object
        # in those cases it is better to issue a warning message

    return redirect('IvaList')


@login_required
def PositionBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm('accounting.delete_position'):
        id_list = request.POST.getlist('instance')
        # This will submit an array of the value attributes of all the
        # checkboxes that have been checked, that is an array of {{obj.id}}

        # Now all that is left is to iterate over the array fetch the
        # object with the ID and delete it.
        for position_id in id_list:
            Position.objects.get(id=position_id).delete()
        # maybe in some other cases it is not possible to delete an object
        # as it may be foreigh key to another object
        # in those cases it is better to issue a warning message

    return redirect('PositionList')


@login_required
def SupplierBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm('accounting.delete_supplier'):
        id_list = request.POST.getlist('instance')
        # This will submit an array of the value attributes of all the
        # checkboxes that have been checked, that is an array of {{obj.id}}

        # Now all that is left is to iterate over the array fetch the
        # object with the ID and delete it.
        for supplier_id in id_list:
            Supplier.objects.get(id=supplier_id).delete()
        # maybe in some other cases it is not possible to delete an object
        # as it may be foreigh key to another object
        # in those cases it is better to issue a warning message

    return redirect('SupplierList')


@login_required
def TaskBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm('accounting.delete_task'):
        id_list = request.POST.getlist('instance')
        # This will submit an array of the value attributes of all the
        # checkboxes that have been checked, that is an array of {{obj.id}}

        # Now all that is left is to iterate over the array fetch the
        # object with the ID and delete it.
        for task_id in id_list:
            Task.objects.get(id=task_id).delete()
        # maybe in some other cases it is not possible to delete an object
        # as it may be foreigh key to another object
        # in those cases it is better to issue a warning message

    return redirect('TaskList')


@login_required
def TitleBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm('accounting.delete_title'):
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

    return redirect('TitleList')


@login_required
def WarehouseBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm('accounting.delete_warehouse'):
        id_list = request.POST.getlist('instance')
        # This will submit an array of the value attributes of all the
        # checkboxes that have been checked, that is an array of {{obj.id}}

        # Now all that is left is to iterate over the array fetch the
        # object with the ID and delete it.
        for warehouse_id in id_list:
            Warehouse.objects.get(id=warehouse_id).delete()
        # maybe in some other cases it is not possible to delete an object
        # as it may be foreigh key to another object
        # in those cases it is better to issue a warning message

    return redirect('WarehouseList')
