from django.urls import path,re_path
from . models import views

urlpattern = [
	re_path(r'^/$',views.cart),
	re_path(r'^add_(\d+)_(\d+)/$',views.add),
	re_path(r'^edit_(\d+)_(\d+)/$',views.edit),
	re_path(r'^delete/(\d+)/$',views.delete),
]
