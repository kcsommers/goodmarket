from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('signup/', views.signup_view, name='signup_view'),
	path('market/', views.market, name='market'),
	path('login/', views.login_view, name="login"),
	path('signup/', views.signup_view, name="signup"),
	path('logout/', views.logout_view, name="logout"),
	path('checkout/', views.checkout, name="checkout"),
	path('item/<int:item_id>', views.show_item, name="show"),
	path('charities/', views.charity, name="charity"),
	path('sell/', views.sell, name="sell"),
	path('cart/', views.cart, name="cart"),
	path('thecart/<int:item_id>/', views.thecart, name="thecart"),
	path('post_item/', views.post_item, name="post_item"),
	path('profile/', views.profile, name="profile"),
	path('profile/update/', views.profile_update, name="profile_update"),
	path('post_profile/', views.post_profile, name="post_profile"),
	path('stripe_redirect/', views.stripe_redirect, name="stripe_redirect"),
	path('cart/delete/<int:item_id>/', views.cart_delete, name="cart_delete")
]