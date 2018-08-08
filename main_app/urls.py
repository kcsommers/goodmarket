from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('market/', views.market, name='market'),
	path('login/', views.login_view, name="login"),
	path('logout/', views.logout_view, name="logout"),
	path('checkout/', views.checkout, name="checkout"),
	path('signup/', views.signup_view, name="signup"),
	path('item/<int:item_id>', views.show_item, name="show"),
	path('charities/', views.charity, name="charity"),
	path('sell/', views.sell, name="sell"),
	path('cart/', views.cart, name="cart"),
	path('post_item/', views.post_item, name="post_item"),
	path('profile/', views.profile, name="profile")
]