from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('login/', views.login_view, name="login"),
	path('logout/', views.logout_view, name="logout"),
	path('checkout/', views.checkout, name="checkout"),
	path('show/', views.show_view, name="show"),
	path('charity/', views.charity_view, name="charity")
]