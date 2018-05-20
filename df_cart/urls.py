from django.urls import path,re_path
from . import views

urlpatterns = [
	re_path(r'^$',views.cart,name='cart'),
	re_path(r'^add_(\d+)_(\d+)/$',views.add,name='cart_add'),
	re_path(r'^edit_(\d+)_(\d+)/$',views.edit,name='cart_edit'),
	re_path(r'^delete/(\d+)/$',views.delete,name='cart_del'),
]
