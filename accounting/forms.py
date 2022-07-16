from django import forms
from django.forms import HiddenInput, DateInput
from .models import *
from .widgets import DatePickerInput, TimePickerInput


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time':
            DateInput(attrs={'type': 'datetime-local'},
                      format='%Y-%m-%dT%H:%M'),
            'end_time':
            DateInput(attrs={'type': 'datetime-local'},
                      format='%Y-%m-%dT%H:%M'),
        }
        labels = {
            'title': 'Título:',
            'description': 'Descrição',
            'start_time': 'Início:',
            'end_time': 'Fim:'
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M', )
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M', )


class SaftForm(forms.ModelForm):

    class Meta:
        model = Saft
        fields = "__all__"

        labels = {
            'zeroStock': 'Inicializar o stock todo a 0',
            'itemProfitRate': 'Taxa Lucro Produtos',
            'month': 'Mês:',
            'file': 'Ficheiro:'
        }


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = "__all__"

        widgets = {
            'format': 'YYYY/MM/DD',
            'dateOfBirth': DatePickerInput(),
        }

        labels = {
            'title': 'Título:',
            'gender': 'Género:',
            'name': 'Nome:',
            'address': 'Morada:',
            'zipCode': 'Código Postal:',
            'city': 'Cidade:',
            'country': 'País:',
            'website': 'Website:',
            'taxNumber': 'NIF:',
            'dateOfBirth': 'Data de Nascimento:',
            'phone': 'Nº Telefone:',
            'contactByEmail': 'Contactar por e-mail',
            'contactBySMS': 'Contactar por SMS',
            'contactByPhone': 'Contactar por Chamada Telefónica'
        }


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = "__all__"

        widgets = {
            'format': 'YYYY/MM/DD',
            'dateOfBirth': DatePickerInput(),
        }

        labels = {
            'title': 'Título:',
            'gender': 'Género:',
            'name': 'Nome:',
            'address': 'Morada:',
            'zipCode': 'Código Postal:',
            'city': 'Cidade:',
            'country': 'País:',
            'taxNumber': 'NIF:',
            'dateOfBirth': 'Data de Nascimento:',
            'phone': 'Nº Telefone:',
            'contactByEmail': 'Contactar por e-mail',
            'contactBySMS': 'Contactar por SMS',
            'contactByPhone': 'Contactar por Chamada Telefónica'
        }


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = "__all__"

        widgets = {
            'format': 'YYYY/MM/DD',
            'date': DatePickerInput(),
        }

        labels = {
            'description': 'Descrição:',
            'cost': 'Valor:',
            'employee': 'Funcionário:',
            'date': 'Data:',
        }


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = "__all__"

        labels = {
            'code': 'Código produto',
            'category': 'Categoria:',
            'tax': 'IVA:',
            'cost': 'Custo(€):',
            'description': 'Descrição:',
            'external_Ref': 'Referência Externa:',
            'weight': 'Peso:',
            'origin': 'Origem:',
            'notes': 'Notas:',
            'supplier_Id': 'Fornecedor:',
            'pvp': 'PVP(€):'
        }


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = "__all__"

        labels = {
            'docNumber': 'Nº fatura:',
            'customer': 'Cliente:',
            'date': 'Data:',
            'tax': 'Taxa IVA:',
            'netTotal': 'Preço (Líquido):',
            'grossTotal': 'Preço (Bruto):'
        }


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = "__all__"

        widgets = {
            'format': 'YYYY/MM/DD',
            'date': DatePickerInput(),
        }

        labels = {
            'quantity': 'Quantidade:',
            'description': 'Descrição:',
            'cost': 'Valor:',
            'supplier': 'Fornecedor:',
            'warehouse': 'Armazém:',
            'date': 'Data:',
        }

class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = "__all__"

        labels = {'receiver': 'Para:', 'msg_content': 'Mensagem:'}
        widgets = {'sender': forms.HiddenInput()}



class PositionForm(forms.ModelForm):

    class Meta:
        model = Position
        fields = "__all__"

        labels = {'name': 'Nome:', 'description': 'Descrição:'}


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = "__all__"

        widgets = {
            'format': 'YYYY/MM/DD',
            'dateOfBirth': DatePickerInput(),
        }

        labels = {
            'name': 'Nome:',
            'address': 'Morada:',
            'zipCode': 'Código Postal:',
            'city': 'Cidade:',
            'country': 'País:',
            'website': 'Website:',
            'taxNumber': 'NIF:',
            'dateOfBirth': 'Data de Nascimento:',
            'phone': 'Nº Telefone:',
            'contactByEmail': 'Contactar por e-mail',
            'contactBySMS': 'Contactar por SMS',
            'contactByPhone': 'Contactar por Chamada Telefónica'
        }


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = "__all__"

        widgets = {
            'format': 'YYYY/MM/DD',
            'startDate': DatePickerInput(),
            'endDate': DatePickerInput(),
            'startTime': TimePickerInput(),
            'endTime': TimePickerInput(),
            'createdBy': HiddenInput()
        }

        labels = {
            'title': 'Título:',
            'description': 'Descrição:',
            'startDate': 'Data Início:',
            'endDate': 'Data Fim:',
            'startTime': 'Hora Início:',
            'endTime': 'Hora Fim:',
            'completed': 'Completada',
            'createdOn': 'Criado em:',
            'assignedTo': 'Atribuída a:'
        }


class WarehouseForm(forms.ModelForm):

    class Meta:
        model = Warehouse
        fields = "__all__"

        labels = {
            'name': 'Nome:',
            'description': 'Descrição:',
            'address': 'Morada:'
        }