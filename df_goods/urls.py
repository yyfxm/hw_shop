from django.urls import path,re_path
from . import views

urlpatterns = [
	path('',views.index,name='index'),
	re_path(r'^list_(\d+)_(\d+)_(\d+)/$',views.list),
	
]
