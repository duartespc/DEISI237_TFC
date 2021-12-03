from django.contrib import admin
from django.urls import path
from django.urls import include, re_path
from nucleos import settings
from django.conf.urls.static import static
from accounting import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<filename>.html', views.html),
	path('costumers/', views.costumerList_view),
	path('costumers/new/', views.costumerNew_view),
	path('titles/', views.titleList_view, name='titleList'),
	path('titles/new/', views.titleNew_view),
	re_path(r'^TitleBulkAction/$', views.TitleBulkAction_view, name='TitleBulkAction'),	
    path('', views.index),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
