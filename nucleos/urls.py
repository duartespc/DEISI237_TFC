from unicodedata import name
from django.contrib import admin
from django.urls import path
from django.urls import include, re_path
from nucleos import settings
from django.conf.urls.static import static
from accounting import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<filename>.html', views.html),
	path('clientes/', views.CustomerList_view, name='CustomerList'),
	path('clientes/edit/<int:customer_id>', views.CustomerEdit_view, name="CustomerEdit"),	
	re_path(r'^CustomerBulkAction/$', views.CustomerBulkAction_view, name='CustomerBulkAction'),
	path('funcionarios/', views.EmployeeList_view, name='EmployeeList'),
	path('funcionarios/edit/<int:employee_id>', views.EmployeeEdit_view, name="EmployeeEdit"),	
	re_path(r'^EmployeeBulkAction/$', views.EmployeeBulkAction_view, name='EmployeeBulkAction'),
	path('inventario/', views.InventoryList_view, name='InventoryList'),
	path('faturas/', views.InvoiceList_view, name='InvoiceList'),
	path('items/', views.ItemList_view, name='ItemList'),
	path('items/edit/<int:item_id>', views.ItemEdit_view, name="ItemEdit"),	
	re_path(r'^ItemBulkAction/$', views.ItemBulkAction_view, name='ItemBulkAction'),
	path('iva/', views.IvaList_view, name='IvaList'),
	path('iva/edit/<int:iva_id>', views.IvaEdit_view, name="Ivadit"),	
	re_path(r'^IvaBulkAction/$', views.IvaBulkAction_view, name='IvaBulkAction'),
	path('pagamentos/', views.PaymentList_view, name='PaymentList'),
	path('cargos/', views.PositionList_view, name='PositionList'),
	path('cargos/edit/<int:position_id>', views.PositionEdit_view, name="PositionEdit"),
	re_path(r'^PositionBulkAction/$', views.PositionBulkAction_view, name='PositionBulkAction'),
	path('fornecedores/', views.SupplierList_view, name='SupplierList'),
	path('fornecedores/edit/<int:supplier_id>', views.SupplierEdit_view, name="SupplierEdit"),
	re_path(r'^SupplierBulkAction/$', views.SupplierBulkAction_view, name='SupplierBulkAction'),
	path('tarefas/', views.TaskList_view, name='TaskList'),
	path('tarefas/edit/<int:task_id>', views.TaskEdit_view, name="TaskEdit"),
	re_path(r'^TaskBulkAction/$', views.TaskBulkAction_view, name='TaskBulkAction'),
	path('titulos/', views.TitleList_view, name='TitleList'),
	path('titulos/edit/<int:title_id>', views.TitleEdit_view, name="TitleEdit"),
	re_path(r'^TitleBulkAction/$', views.TitleBulkAction_view, name='TitleBulkAction'),
	path('armazens/', views.WarehouseList_view, name='WarehouseList'),
	path('armazens/edit/<int:warehouse_id>', views.WarehouseEdit_view, name="WarehouseEdit"),	
	re_path(r'^WarehouseBulkAction/$', views.WarehouseBulkAction_view, name='WarehouseBulkAction'),
	path('usuario/info/', views.UserInfo_view, name="UserInfo"),	
    path('', views.index),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
