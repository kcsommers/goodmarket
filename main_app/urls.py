from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('market/', views.market, name='market'),
	path('login/', views.login_view, name="login"),
	path('logout/', views.logout_view, name="logout"),
	path('checkout/', views.checkout, name="checkout"),
]