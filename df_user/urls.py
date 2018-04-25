from django.urls import path,re_path
from . import views

urlpatterns = [
	re_path(r'^register/$',views.register),
	re_path(r'^register_handle/$',views.register_handle),
	re_path(r'^login/$',views.login),
	re_path(r'^login_handle/$',views.login_handle),
	re_path(r'^logout/$',views.logout),
	re_path(r'^user_center_info/$',views.user_center_info),
	re_path(r'^user_center_site/$',views.user_center_site),
	re_path(r'^user_center_order/(\d+)/$',views.user_center_order),
]
