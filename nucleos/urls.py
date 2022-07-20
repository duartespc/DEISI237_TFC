from unicodedata import name
from django.contrib import admin
from django.urls import path
from django.urls import include, re_path
from nucleos import settings
from django.conf.urls.static import static
from accounting import views

urlpatterns = [
	re_path(r'^event/new/', views.event, name='event_new'),
    re_path(r'eventos/editar/<event_id>/', views.event, name='event_edit'),
    re_path(r'calendario/', views.CalendarView.as_view(), name='calendar'), # here
    path('admin/', admin.site.urls, name="AdminPage"),
    path('<filename>.html', views.html),
	path('clientes/', views.CustomerList_view, name='CustomerList'),
	path('clientes/edit/<int:customer_id>', views.CustomerEdit_view, name="CustomerEdit"),	
	re_path(r'^CustomerBulkAction/$', views.CustomerBulkAction_view, name='CustomerBulkAction'),
	path('pagamentos/', views.PaymentList_view, name='PaymentList'),
	path('pagamentos/edit/<int:payment_id>', views.PaymentEdit_view, name="PaymentEdit"),
	re_path(r'^PaymentBulkAction/$', views.PaymentBulkAction_view, name='PaymentBulkAction'),
	path('encomendas/', views.OrderList_view, name='OrderList'),
	path('encomendas/edit/<int:order_id>', views.OrderEdit_view, name="OrderEdit"),
	re_path(r'^OrderBulkAction/$', views.OrderBulkAction_view, name='OrderBulkAction'),
	path('funcionarios/', views.EmployeeList_view, name='EmployeeList'),
	path('funcionarios/edit/<int:employee_id>', views.EmployeeEdit_view, name="EmployeeEdit"),	
	re_path(r'^EmployeeBulkAction/$', views.EmployeeBulkAction_view, name='EmployeeBulkAction'),
	path('inventario/', views.InventoryList_view, name='InventoryList'),
	path('faturas/', views.InvoiceList_view, name='InvoiceList'),
	path('items/', views.ItemList_view, name='ItemList'),
	path('items/edit/<int:item_id>', views.ItemEdit_view, name="ItemEdit"),
	path('faturas/edit/<int:invoice_id>', views.InvoiceEdit_view, name="InvoiceEdit"),	
	re_path(r'^InvoiceBulkAction/$', views.InvoiceBulkAction_view, name='InvoiceBulkAction'),
	re_path(r'^ItemBulkAction/$', views.ItemBulkAction_view, name='ItemBulkAction'),
	path('cargos/', views.PositionList_view, name='PositionList'),
	path('cargos/edit/<int:position_id>', views.PositionEdit_view, name="PositionEdit"),
	re_path(r'^PositionBulkAction/$', views.PositionBulkAction_view, name='PositionBulkAction'),
	path('fornecedores/', views.SupplierList_view, name='SupplierList'),
	path('fornecedores/edit/<int:supplier_id>', views.SupplierEdit_view, name="SupplierEdit"),
	path('saft/', views.SaftList_view, name='SaftList'),
	re_path(r'^SaftBulkAction/$', views.SaftBulkAction_view, name='SaftBulkAction'),
	re_path(r'^SupplierBulkAction/$', views.SupplierBulkAction_view, name='SupplierBulkAction'),
	path('tarefas/', views.TaskList_view, name='TaskList'),
	path('tarefas/edit/<int:task_id>', views.TaskEdit_view, name="TaskEdit"),
	re_path(r'^TaskBulkAction/$', views.TaskBulkAction_view, name='TaskBulkAction'),
	path('armazens/', views.WarehouseList_view, name='WarehouseList'),
	path('armazens/edit/<int:warehouse_id>', views.WarehouseEdit_view, name="WarehouseEdit"),	
	re_path(r'^WarehouseBulkAction/$', views.WarehouseBulkAction_view, name='WarehouseBulkAction'),
	path('usuario/info/', views.UserInfo_view, name="UserInfo"),
	path('relatorios/', views.ReportList_view, name="ReportList"),
	path('mensagens/', views.MessageList_view, name="MessageList"),
	path('email/', views.EmailList_view, name="EmailList"),
	re_path(r'^MessageBulkAction/$', views.MessageBulkAction_view, name="MessageBulkAction"),
	re_path(r'^EmailBulkAction/$', views.EmailBulkAction_view, name="EmailBulkAction"),	
    path('', views.index, name='index'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
