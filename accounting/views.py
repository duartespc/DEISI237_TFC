from asyncio.windows_events import NULL
import calendar
from email import message
from email.message import EmailMessage
from hashlib import new
import json
from os import F_OK
import pdb
from pyexpat.errors import messages
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, render
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from .utils import Calendar
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django_q.tasks import async_task

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, permission_required
from datetime import date, datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe

from .models import *
from .utils import Calendar

from .forms import *
from .models import *
from .saft import *
from .tasks import *
from django.db.models import Sum


@login_required
def index(request):
    return html(request, "index")


def html(request, filename):
    current_user = request.user

    if current_user.is_anonymous and filename != "login":
        return redirect("/login.html")

    if current_user.is_anonymous:
        context = {"filename": filename, "collapse": ""}
    else:
        inbox = Message.objects.filter(receiver=current_user)
        context = {"filename": filename, 'inbox': inbox, "collapse": ""}

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

    if filename == "index":
        inbox = Message.objects.filter(receiver=current_user)
        #month = datetime.datetime.now().month
        #year = datetime.datetime.now().year

        month=8
        year=2021

        allMonthsSales = []
        allMonthsStockExpenses = []
        allMonthsPaymentExpenses = []
        # monthsGains = Sales - Expenses
        allMonthsGains = []
        # monthsExpenses = Cost of stock + payments (like salaries, rent,...)
        allMonthsExpenses = []

        for i in range(1, 13):
            sales = Invoice.objects.filter(date__year=year,
                                           date__month=i).aggregate(
                                               Sum('netTotal'))
            stock = ItemInput.objects.filter(date__year=year,
                                              date__month=i).aggregate(
                                                  Sum('total'))
            payments = Payment.objects.filter(date__year=year,
                                              date__month=i).aggregate(
                                                  Sum('cost'))
            totalSales = sales['netTotal__sum']
            totalStock = stock['total__sum']
            totalPayments = payments['cost__sum']
            if totalSales == None:
                totalSales = 0
            if totalStock == None:
                totalStock = 0
            if totalPayments == None:
                totalPayments = 0
            allMonthsSales.append(totalSales)
            allMonthsStockExpenses.append(totalStock)
            allMonthsPaymentExpenses.append(totalPayments)
            allMonthsGains.append(totalSales - totalStock - totalPayments)
            allMonthsExpenses.append(totalStock + totalPayments)

        yearSales = Invoice.objects.filter(date__year=year).aggregate(
            Sum('netTotal'))
        yearStockExpenses = ItemInput.objects.filter(
            date__year=year).aggregate(Sum('total'))
        yearPaymentExpenses = Payment.objects.filter(
            date__year=year).aggregate(Sum('cost'))
        yearSales = yearSales['netTotal__sum']
        yearStock = yearStockExpenses['total__sum']
        yearPayments = yearPaymentExpenses['cost__sum']

        if yearSales == None:
            yearSales = 0
        if yearStock == None:
            yearStock = 0
        if yearPayments == None:
            yearPayments = 0

        # We use [month-1] because months are 1-12 and the list goes from 0-11
        monthSales = allMonthsSales[month - 1]
        monthGains = allMonthsSales[month - 1] - allMonthsStockExpenses[
            month - 1] - allMonthsPaymentExpenses[month - 1]
        yearGains = yearSales - yearStock - yearPayments

        allMonthsGains = json.dumps(allMonthsGains)
        allMonthsExpenses = json.dumps(allMonthsExpenses)
        allMonthsSales = json.dumps(allMonthsSales)

        context = {
            "filename": filename,
            'monthSales': monthSales,
            'monthGains': monthGains,
            'yearSales': yearSales,
            'yearGains': yearGains,
            'allMonthsSales': allMonthsSales,
            'allMonthsGains': allMonthsGains,
            'allMonthsExpenses': allMonthsExpenses,
            'month': month,
            'year': year,
            'inbox': inbox,
            "collapse": ""
        }

    print(filename, request.method)
    return render(request, f"{filename}.html", context=context)


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))

    return render(request, 'event.html', {'form': form})


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return date.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendarList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['collapse'] = 'Items'

        return context


@login_required
@permission_required('accounting.add_saft')
def handle_uploaded_saft(request, f, filename, itemProfitRate, zeroStock):
    with open(f'static/data/\saft/{filename}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    mysaft = getSaft(f"static/data/saft/{filename}")

    # Add and Update Items (products)
    for item in mysaft["products"]:
        try:
            existingItem = Item.objects.get(code=item['ProductCode'])
            existingItem.code = item['ProductCode']
            existingItem.description = item['ProductDescription']
            existingItem.pvp = item['UnitPrice']
            existingItem.tax = item['TaxPercentage']
            existingItem.cost = round(
                (
                    float(item['UnitPrice'])
                    *  # Item Profit Rate is a percentage Ex: 30% so we have to divide it by 100
                    (1 - float(itemProfitRate) / 100)),
                2)
            existingItem.save()
        except Item.DoesNotExist:
            existingItem = Item()
            existingItem.code = item['ProductCode']
            existingItem.description = item['ProductDescription']
            existingItem.pvp = item['UnitPrice']
            existingItem.tax = item['TaxPercentage']
            existingItem.cost = round(
                (
                    float(item['UnitPrice'])
                    *  # Item Profit Rate is a percentage Ex: 30% so we have to divide it by 100
                    (1 - float(itemProfitRate) / 100)),
                2)
            existingItem.save()

    # Add and Update Clients
    for client in mysaft["clients"]:
        try:
            existingCustomer = Customer.objects.get(
                taxNumber=client["CustomerTaxID"])
            existingCustomer.name = client["CompanyName"]
            existingCustomer.address = client["BillingAddress"][
                "AddressDetail"]
            existingCustomer.city = client["BillingAddress"]["City"]
            existingCustomer.zipCode = client["BillingAddress"]["PostalCode"]
            existingCustomer.country = client["BillingAddress"]["Country"]
            existingCustomer.save()
        except Customer.DoesNotExist:
            existingCustomer = Customer(taxNumber=client["CustomerTaxID"])
            existingCustomer.name = client['CompanyName']
            existingCustomer.address = client["BillingAddress"][
                "AddressDetail"]
            existingCustomer.city = client["BillingAddress"]["City"]
            existingCustomer.zipCode = client["BillingAddress"]["PostalCode"]
            existingCustomer.country = client["BillingAddress"]["Country"]
            existingCustomer.save()


# Add and Update Invoices
    for invoice in mysaft["invoices"]:
        if invoice['InvoiceType'] != "FS":
            continue
        try:
            existingInvoice = Invoice.objects.get(
                docNumber=invoice["InvoiceNo"])
            existingInvoice.customer = Customer.objects.get(
                taxNumber=invoice["CustomerID"])
            existingInvoice.date = invoice["InvoiceDate"]
            existingInvoice.tax = invoice["DocumentTotals"]["TaxPayable"]
            existingInvoice.netTotal = invoice["DocumentTotals"]["NetTotal"]
            existingInvoice.grossTotal = invoice["DocumentTotals"][
                "GrossTotal"]

            for item in invoice["items"]:
                newItemOutput = ItemOutput()
                newItemOutput.date = invoice["InvoiceDate"]
                newItemOutput.item = Item.objects.get(code=item["ProductCode"])
                newItemOutput.tax = float(item["Tax"]["TaxPercentage"])
                newItemOutput.cost = float(item["UnitPrice"])
                newItemOutput.quantity = float(item["Quantity"])
                newItemOutput.total = newItemOutput.cost * newItemOutput.quantity
                #newItemOutput.input =
                #newItemOutput.warehouse =
                newInvoiceItem = InvoiceItem()
                newInvoiceItem.invoice = existingInvoice
                newInvoiceItem.output = newItemOutput
                existingInvoice.save()
                newItemOutput.save()
                newInvoiceItem.save()
                if zeroStock:
                    newItemInput = ItemInput()
                    newItemInput.item = Item.objects.get(
                        code=item["ProductCode"])
                    newItemInput.cost = round(
                        (
                            float(item['UnitPrice'])
                            *  # Item Profit Rate is a percentage Ex: 30% so we have to divide it by 100
                            (1 - float(itemProfitRate) / 100)),
                        2)
                    newItemInput.date = invoice["InvoiceDate"]
                    newItemInput.tax = float(item["Tax"]["TaxPercentage"])
                    newItemInput.quantity = float(item["Quantity"])
                    newItemInput.total = newItemInput.cost * newItemInput.quantity
                    newItemInput.save()
        except Invoice.DoesNotExist:
            existingInvoice = Invoice(docNumber=invoice["InvoiceNo"])
            existingInvoice.customer = Customer.objects.get(
                taxNumber=invoice["CustomerID"])
            existingInvoice.date = invoice["InvoiceDate"]
            existingInvoice.tax = invoice["DocumentTotals"]["TaxPayable"]
            existingInvoice.netTotal = invoice["DocumentTotals"]["NetTotal"]
            existingInvoice.grossTotal = invoice["DocumentTotals"][
                "GrossTotal"]

            for item in invoice["items"]:
                newItemOutput = ItemOutput()
                newItemOutput.date = invoice["InvoiceDate"]
                newItemOutput.item = Item.objects.get(code=item["ProductCode"])
                newItemOutput.tax = float(item["Tax"]["TaxPercentage"])
                newItemOutput.cost = float(item["UnitPrice"])
                newItemOutput.quantity = float(item["Quantity"])
                newItemOutput.total = newItemOutput.cost * newItemOutput.quantity
                #newItemOutput.input =
                #newItemOutput.warehouse =
                newInvoiceItem = InvoiceItem()
                newInvoiceItem.invoice = existingInvoice
                newInvoiceItem.output = newItemOutput
                existingInvoice.save()
                newItemOutput.save()
                newInvoiceItem.save()
                if zeroStock:
                    newItemInput = ItemInput()
                    newItemInput.item = Item.objects.get(
                        code=item["ProductCode"])
                    newItemInput.cost = round(
                        (
                            float(item['UnitPrice'])
                            *  # Item Profit Rate is a percentage Ex: 30% so we have to divide it by 100
                            (1 - float(itemProfitRate) / 100)),
                        2)
                    newItemInput.date = invoice["InvoiceDate"]
                    newItemInput.tax = float(item["Tax"]["TaxPercentage"])
                    newItemInput.quantity = float(item["Quantity"])
                    newItemInput.total = newItemInput.cost * newItemInput.quantity
                    newItemInput.save()

    current_user = request.user
    email = EmailMessage(
        'DEISI237 - Upload do ficheiro SAF-T concluido!',
        'O upload do ficheiro SAF-T foi concluído com sucesso, todas as informações já estão disponíveis para visualização.',
        'deisi237@teste.pt', [current_user.email],
        headers={'Reply-To': 'geral@eltuktukhero.pt'})
    email.send(fail_silently=False)


@login_required
@permission_required('accounting.view_customer')
def CustomerList_view(request):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)
    form = CustomerForm(request.POST or None, request.FILES or None)
    if form.is_valid() and current_user.has_perm('accounting.add_customer'):
        form.save()
        return redirect('CustomerList')
    customers = Customer.objects.all()
    context = {
        'form': form,
        'inbox': inbox,
        'customers': customers,
        'collapse': 'Sales'
    }

    return render(request=request,
                  template_name="customerList.html",
                  context=context)


@login_required
@permission_required('accounting.add_email')
def EmailList_view(request):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)
    emails = Email.objects.all()

    form = EmailForm(request.POST or None,
                     request.FILES or None,
                     initial={'author': current_user})

    if form.is_valid():
        subject = form.cleaned_data['subject']
        content = form.cleaned_data['content']
        form.save()

        receivers = []
        for customer in Customer.objects.all():
            if customer.contactByEmail:
                receivers.append(customer.email)

        email = EmailMessage(subject,
                             content,
                             'deisi237@teste.pt',
                             receivers,
                             headers={'Reply-To': 'deisi237@teste.pt'})

        email.send(fail_silently=False)
        return redirect('EmailList')

    context = {'form': form, 'inbox': inbox, 'emails': emails}

    return render(request=request,
                  template_name="emailList.html",
                  context=context)


@login_required
@permission_required('accounting.view_employee')
def EmployeeList_view(request):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)
    form = EmployeeForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_employee'):
        form.save()
        return redirect('EmployeeList')
    employees = Employee.objects.all()
    context = {
        'form': form,
        'inbox': inbox,
        'employees': employees,
        'collapse': 'HR'
    }

    return render(request=request,
                  template_name="employeeList.html",
                  context=context)


@login_required
def MessageList_view(request):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)
    sentBox = Message.objects.filter(sender=current_user)

    form = MessageForm(request.POST or None,
                       request.FILES or None,
                       initial={'sender': current_user})

    if form.is_valid():
        form.save()
        return redirect('MessageList')

    context = {'form': form, 'inbox': inbox, 'sentBox': sentBox}

    return render(request=request,
                  template_name="messageList.html",
                  context=context)


@login_required
@permission_required('accounting.view_payment')
def PaymentList_view(request):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)
    form = PaymentForm(request.POST or None, request.FILES or None)
    if form.is_valid() and current_user.has_perm('accounting.add_payment'):
        form.save()
        return redirect('PaymentList')
    payments = Payment.objects.all()
    context = {
        'form': form,
        'inbox': inbox,
        'payments': payments,
        'collapse': 'Purchases'
    }

    return render(request=request,
                  template_name="paymentList.html",
                  context=context)


@login_required
@permission_required('accounting.view_item')
def ItemList_view(request):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)
    form = ItemForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_item'):
        form.save()
        return redirect('ItemList')

    items = Item.objects.all()
    context = {
        'form': form,
        'inbox': inbox,
        'items': items,
        'collapse': 'Items'
    }

    return render(request=request,
                  template_name="itemList.html",
                  context=context)


@login_required
@permission_required('accounting.view_item')
def InventoryList_view(request):
    current_user = request.user
    items = Item.objects.all()
    inbox = Message.objects.filter(receiver=current_user)

    # quantity in stock = count(itemInputs) - count(itemOutputs)
    for item in items:
        quantityInput = 0
        quantityOutput = 0
        itemInputs = ItemInput.objects.filter(item=item)
        itemOutputs = ItemOutput.objects.filter(item=item)
        for itemInput in itemInputs:
            quantityInput += itemInput.quantity
        for itemOutput in itemOutputs:
            quantityOutput += itemOutput.quantity
        item.quantity = quantityInput - quantityOutput

    context = {'items': items, 'inbox': inbox, 'collapse': 'Items'}

    return render(request=request,
                  template_name="inventoryList.html",
                  context=context)


@login_required
@permission_required('accounting.view_invoice')
def InvoiceList_view(request):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)

    form = ItemForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_invoice'):
        form.save()
        return redirect('InvoiceList')

    invoices = Invoice.objects.all()
    context = {
        'form': form,
        'inbox': inbox,
        'invoices': invoices,
        'collapse': 'Customers'
    }

    return render(request=request,
                  template_name="invoiceList.html",
                  context=context)


# Basically this function just creates as many ItemInputs(Purchases) as there are ItemOutputs(Sales)
# This way we can set the quantity in stock to 0 to all Items before getting the correct ammount (mannually, since we have no structured data of inventory bought)
@login_required
@permission_required('accounting.add_saft')
def restock(request):

    items = Item.objects.all()

    # 1st check how many items were sold
    # 2nd "enter" that many items so stock is at 0

    for item in items:
        quantityOutput = 0
        itemOutputs = ItemOutput.objects.filter(item=item)

        for itemOutput in itemOutputs:
            quantityOutput += itemOutput.quantity

        newItemInput = ItemInput()
        newItemInput.item = item
        newItemInput.cost = item.cost
        newItemInput.date = date.today()
        newItemInput.tax = item.tax
        newItemInput.quantity = quantityOutput
        newItemInput.total = item.cost * quantityOutput
        newItemInput.save()


@login_required
@permission_required('accounting.view_order')
def OrderList_view(request):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)
    form = OrderForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_order'):
        itemCode = form.cleaned_data['item']
        quantity = form.cleaned_data['quantity']
        cost = form.cleaned_data['cost']
        date = form.cleaned_data['date']
        tax = form.cleaned_data['tax']
        description = form.cleaned_data['description']
        form.save()
        item = Item.objects.get(code=itemCode)
        order = Order.objects.get(item=item,
                                  quantity=quantity,
                                  cost=cost,
                                  date=date,
                                  description=description)
        newItemInput = ItemInput()
        newItemInput.quantity = quantity
        newItemInput.item = item
        newItemInput.order = order
        newItemInput.date = date
        newItemInput.cost = cost
        newItemInput.tax = tax
        newItemInput.total = float(cost) * float(quantity)
        newItemInput.save()

        return redirect('OrderList')

    orders = Order.objects.all()
    context = {
        'form': form,
        'inbox': inbox,
        'orders': orders,
        'collapse': 'Purchases'
    }

    return render(request=request,
                  template_name="orderList.html",
                  context=context)


@login_required
@permission_required('accounting.view_position')
def PositionList_view(request):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)
    form = PositionForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_position'):
        form.save()
        return redirect('PositionList')

    positions = Position.objects.all()
    context = {
        'form': form,
        'inbox': inbox,
        'positions': positions,
        'collapse': 'HR'
    }

    return render(request=request,
                  template_name="positionList.html",
                  context=context)


@login_required
@permission_required('accounting.view_task')
def TaskList_view(request):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)
    form = TaskForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_task'):
        post = form.save(commit=False)
        post.createdBy = request.user
        post.updatedOn = datetime.now()
        post.save()
        return redirect('TaskList')

    tasks = Task.objects.all()
    context = {
        'form': form,
        'inbox': inbox,
        'tasks': tasks,
        'collapse': 'Extras'
    }

    return render(request=request,
                  template_name="taskList.html",
                  context=context)


@login_required
@permission_required('accounting.view_warehouse')
def WarehouseList_view(request):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)
    form = WarehouseForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_warehouse'):
        form.save()
        return redirect('WarehouseList')

    warehouses = Warehouse.objects.all()
    context = {
        'form': form,
        'inbox': inbox,
        'warehouses': warehouses,
        'collapse': 'Items'
    }

    return render(request=request,
                  template_name="warehouseList.html",
                  context=context)


@login_required
@permission_required('accounting.view_supplier')
def ReportList_view(request):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)

    #form = SupplierForm(request.POST or None, request.FILES or None)

    #if form.is_valid() and current_user.has_perm('accounting.add_supplier'):
    #form.save()
    #return redirect('SupplierList')

    #suppliers = Supplier.objects.all()
    context = {'collapse': 'Customers', 'inbox': inbox}

    return render(request=request,
                  template_name="reportList.html",
                  context=context)


@login_required
@permission_required('accounting.view_supplier')
def SupplierList_view(request):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)
    form = SupplierForm(request.POST or None, request.FILES or None)

    if form.is_valid() and current_user.has_perm('accounting.add_supplier'):
        form.save()
        return redirect('SupplierList')

    suppliers = Supplier.objects.all()
    context = {
        'form': form,
        'suppliers': suppliers,
        'collapse': 'Customers',
        'inbox': inbox
    }

    return render(request=request,
                  template_name="supplierList.html",
                  context=context)


@login_required
def UserInfo_view(request):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)

    context = {'user': current_user, 'inbox': inbox}
    return render(request=request,
                  template_name="userInfo.html",
                  context=context)


@permission_required('accounting.change_customer')
@login_required
def CustomerEdit_view(request, customer_id):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)
    customer = Customer.objects.get(id=customer_id)
    invoices = Invoice.objects.filter(customer=customer)

    # Edit object of form

    form = CustomerForm(request.POST or None, instance=customer)

    if request.POST and form.is_valid():
        form.save()
        return redirect('CustomerList')

    context = {
        'form': form,
        'inbox': inbox,
        'invoices': invoices,
        'customer': customer,
        'collapse': 'Sales'
    }

    return render(request, 'customerEdit.html', context=context)


@login_required
@permission_required('accounting.delete_email')
def EmailBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST':
        id_list = request.POST.getlist('instance')
        # This will submit an array of the value attributes of all the
        # checkboxes that have been checked, that is an array of {{obj.id}}

        # Now all that is left is to iterate over the array fetch the
        # object with the ID and delete it.
        for email_id in id_list:
            Email.objects.get(id=email_id).delete()
        # maybe in some other cases it is not possible to delete an object
        # as it may be foreigh key to another object
        # in those cases it is better to issue a warning message

    return redirect('EmailList')


@permission_required('accounting.change_employee')
@login_required
def EmployeeEdit_view(request, employee_id):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)

    # Edit object of form
    employee = Employee.objects.get(id=employee_id)

    form = EmployeeForm(request.POST or None, instance=employee)

    if request.POST and form.is_valid():
        form.save()
        return redirect('EmployeeList')

    context = {
        'form': form,
        'inbox': inbox,
        'employee': employee,
        'collapse': 'HR'
    }

    return render(request, 'employeeEdit.html', context=context)


@permission_required('accounting.change_payment')
@login_required
def PaymentEdit_view(request, payment_id):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)

    # Edit object of form
    payment = Payment.objects.get(id=payment_id)

    form = PaymentForm(request.POST or None, instance=payment)

    if request.POST and form.is_valid():
        form.save()
        return redirect('PaymentList')

    context = {
        'form': form,
        'inbox': inbox,
        'payment': payment,
        'collapse': 'Customers'
    }

    return render(request, 'paymentEdit.html', context=context)


@permission_required('accounting.change_item')
@login_required
def ItemEdit_view(request, item_id):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)

    # Edit object of form
    item = Item.objects.get(id=item_id)

    form = ItemForm(request.POST or None, instance=item)

    if request.POST and form.is_valid():
        form.save()
        return redirect('ItemList')

    context = {'form': form, 'inbox': inbox, 'item': item, 'collapse': 'Items'}

    return render(request, 'itemEdit.html', context=context)


@permission_required('accounting.change_invoice')
@login_required
def InvoiceEdit_view(request, invoice_id):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)

    # Edit object of form
    invoice = Invoice.objects.get(id=invoice_id)

    items = InvoiceItem.objects.filter(invoice=invoice)

    form = InvoiceForm(request.POST or None, instance=invoice)

    if request.POST and form.is_valid() and current_user.has_perm(
            'accounting.edit_invoice'):
        form.save()
        return redirect('InvoiceList')

    context = {
        'form': form,
        'invoice': invoice,
        'items': items,
        'inbox': inbox,
        'collapse': 'Sales'
    }

    return render(request, 'invoiceEdit.html', context=context)


@permission_required('accounting.change_order')
@login_required
def OrderEdit_view(request, order_id):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)

    # Edit object of form
    order = Order.objects.get(id=order_id)
    itemInput = ItemInput.objects.get(order=order)

    form = OrderForm(request.POST or None, instance=order)

    if request.POST and form.is_valid() and current_user.has_perm(
            'accounting.edit_order'):
        quantity = form.cleaned_data['quantity']
        form.save()
        itemInput.quantity = quantity
        itemInput.save()
        return redirect('OrderList')

    context = {
        'form': form,
        'inbox': inbox,
        'order': order,
        'collapse': 'Customers'
    }

    return render(request, 'orderEdit.html', context=context)


@permission_required('accounting.change_position')
@login_required
def PositionEdit_view(request, position_id):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)

    # Edit object of form
    position = Position.objects.get(id=position_id)

    form = PositionForm(request.POST or None, instance=position)

    if request.POST and form.is_valid() and current_user.has_perm(
            'accounting.edit_position'):
        form.save()
        return redirect('PositionList')

    context = {
        'form': form,
        'inbox': inbox,
        'position': position,
        'collapse': 'HR'
    }

    return render(request, 'positionEdit.html', context=context)


@permission_required('accounting.view_saft')
@login_required
def SaftList_view(request):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)
    entries = Saft.objects.all()

    form = SaftForm(request.POST or None, request.FILES or None)
    if form.is_valid() and current_user.has_perm('accounting.add_saft'):
        itemProfitRate = form.cleaned_data['itemProfitRate']
        zeroStock = form.cleaned_data['zeroStock']
        form.save()
        handle_uploaded_saft(request, request.FILES['file'],
                             request.FILES['file'].name, itemProfitRate,
                             zeroStock)
        #async_task(handle_uploaded_saft, request, itemProfitRate, zeroStock)
        return redirect('SaftList')

    context = {'form': form, 'inbox': inbox, 'entries': entries}
    return render(request=request,
                  template_name="upload.html",
                  context=context)


@permission_required('accounting.change_supplier')
@login_required
def SupplierEdit_view(request, supplier_id):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)

    # Edit object of form
    supplier = Supplier.objects.get(id=supplier_id)

    form = SupplierForm(request.POST or None, instance=supplier)

    if request.POST and form.is_valid() and current_user.has_perm(
            'accounting.edit_supplier'):
        form.save()
        return redirect('SupplierList')

    context = {
        'form': form,
        'inbox': inbox,
        'supplier': supplier,
        'collapse': 'Customers'
    }

    return render(request, 'supplierEdit.html', context=context)


@permission_required('accounting.change_task')
@login_required
def TaskEdit_view(request, task_id):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)

    # Edit object of form
    task = Task.objects.get(id=task_id)

    form = TaskForm(request.POST or None, instance=task)

    if request.POST and form.is_valid() and current_user.has_perm(
            'accounting.edit_task'):
        form.save()
        return redirect('TaskList')

    context = {'form': form, 'inbox': inbox, 'task': task}

    return render(request, 'taskEdit.html', context=context)


@permission_required('accounting.change_warehouse')
@login_required
def WarehouseEdit_view(request, warehouse_id):
    current_user = request.user
    inbox = Message.objects.filter(receiver=current_user)

    # Edit object of form
    warehouse = Warehouse.objects.get(id=warehouse_id)

    form = WarehouseForm(request.POST or None, instance=warehouse)

    if request.POST and form.is_valid() and current_user.has_perm(
            'accounting.edit_warehouse'):
        form.save()
        return redirect('WarehouseList')

    context = {
        'form': form,
        'inbox': inbox,
        'warehouse': warehouse,
        'collapse': 'Items'
    }

    return render(request, 'warehouseEdit.html', context=context)


@permission_required('accounting.delete_customer')
@login_required
def CustomerBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm(
            'accounting.delete_customer'):
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
def MessageBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST':
        id_list = request.POST.getlist('instance')
        # This will submit an array of the value attributes of all the
        # checkboxes that have been checked, that is an array of {{obj.id}}

        # Now all that is left is to iterate over the array fetch the
        # object with the ID and delete it.
        for message_id in id_list:
            Message.objects.get(id=message_id).delete()
        # maybe in some other cases it is not possible to delete an object
        # as it may be foreigh key to another object
        # in those cases it is better to issue a warning message

    return redirect('MessageList')


@permission_required('accounting.delete_employee')
@login_required
def EmployeeBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm(
            'accounting.delete_employee'):
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


@permission_required('accounting.delete_payment')
@login_required
def PaymentBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm(
            'accounting.delete_payment'):
        id_list = request.POST.getlist('instance')
        # This will submit an array of the value attributes of all the
        # checkboxes that have been checked, that is an array of {{obj.id}}

        # Now all that is left is to iterate over the array fetch the
        # object with the ID and delete it.
        for payment_id in id_list:
            Payment.objects.get(id=payment_id).delete()
        # maybe in some other cases it is not possible to delete an object
        # as it may be foreigh key to another object
        # in those cases it is better to issue a warning message

    return redirect('PaymentList')


@permission_required('accounting.delete_item')
@login_required
def ItemBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm(
            'accounting.delete_item'):
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


@permission_required('accounting.delete_invoice')
@login_required
def InvoiceBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm(
            'accounting.delete_invoice'):
        id_list = request.POST.getlist('instance')
        # This will submit an array of the value attributes of all the
        # checkboxes that have been checked, that is an array of {{obj.id}}

        # Now all that is left is to iterate over the array fetch the
        # object with the ID and delete it.
        for invoice_id in id_list:
            Invoice.objects.get(id=invoice_id).delete()
        # maybe in some other cases it is not possible to delete an object
        # as it may be foreigh key to another object
        # in those cases it is better to issue a warning message

    return redirect('InvoiceList')


@permission_required('accounting.delete_order')
@login_required
def OrderBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm(
            'accounting.delete_order'):
        id_list = request.POST.getlist('instance')
        # This will submit an array of the value attributes of all the
        # checkboxes that have been checked, that is an array of {{obj.id}}

        # Now all that is left is to iterate over the array fetch the
        # object with the ID and delete it.
        for order_id in id_list:
            Order.objects.get(id=order_id).delete()
        # maybe in some other cases it is not possible to delete an object
        # as it may be foreigh key to another object
        # in those cases it is better to issue a warning message

    return redirect('OrderList')


@permission_required('accounting.delete_position')
@login_required
def PositionBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm(
            'accounting.delete_position'):
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


@permission_required('accounting.delete_saft')
@login_required
def SaftBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm(
            'accounting.delete_saft'):
        id_list = request.POST.getlist('instance')
        # This will submit an array of the value attributes of all the
        # checkboxes that have been checked, that is an array of {{obj.id}}

        # Now all that is left is to iterate over the array fetch the
        # object with the ID and delete it.
        for saft_id in id_list:
            Saft.objects.get(id=saft_id).delete()
        # maybe in some other cases it is not possible to delete an object
        # as it may be foreigh key to another object
        # in those cases it is better to issue a warning message

    return redirect('SaftList')


@permission_required('accounting.delete_supplier')
@login_required
def SupplierBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm(
            'accounting.delete_supplier'):
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


@permission_required('accounting.delete_task')
@login_required
def TaskBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm(
            'accounting.delete_task'):
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


@permission_required('accounting.delete_warehouse')
@login_required
def WarehouseBulkAction_view(request, id=None):
    current_user = request.user

    if request.method == 'POST' and current_user.has_perm(
            'accounting.delete_warehouse'):
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
