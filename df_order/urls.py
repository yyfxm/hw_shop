from django.urls import path,re_path
from . import views

urlpatterns = [
	re_path(r'^$',views.order),
	re_path(r'^push/$',views.order_handle),
]
