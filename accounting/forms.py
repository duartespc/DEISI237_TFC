from django import forms
from django.forms import widgets
from .models import *
from .widgets import DatePickerInput, TimePickerInput


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = "__all__"

        widgets = {
            'format': 'YYYY/MM/DD',
            'dateOfBirth' : DatePickerInput(),
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
            'dateOfBirth' : DatePickerInput(),
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


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = "__all__"

        labels = {
            'category': 'Categoria:',
            'iva': 'IVA:',
            'cost': 'Custo(€):',
            'unit': 'Unidade:',
            'description': 'Descrição:',
            'external_ref': 'Referência Externa:',
            'weight': 'Peso:',
            'origin': 'Origem:',
            'notes': 'Notas:',
            'supplier_Id': 'Fornecedor:',
            'pvp': 'PVP(€):'
        }


class IvaForm(forms.ModelForm):

    class Meta:
        model = Iva
        fields = "__all__"

        labels = {'rate': 'Taxa:', 'name': 'Nome:'}

    def __init__(self, *args, **kwargs):
        super(IvaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


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
            'dateOfBirth' : DatePickerInput(),
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

            'startDate' : DatePickerInput(),
            'endDate' : DatePickerInput(),
            'startTime' : TimePickerInput(),
            'endTime' : TimePickerInput(),
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
            'updatedOn': 'Atualizado em:',
            'createdBy': 'Criada por:',
            'assignedTo': 'Atribuída a:'
        }


class TitleForm(forms.ModelForm):

    class Meta:
        model = Title
        fields = "__all__"

        labels = {'title': 'Título:'}


class WarehouseForm(forms.ModelForm):

    class Meta:
        model = Warehouse
        fields = "__all__"

        labels = {
            'name': 'Nome:',
            'description': 'Descrição:',
            'address': 'Morada:'
        }