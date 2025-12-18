from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('contacts/', views.contacts, name='contacts'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/register/', views.register_api, name='register_api'),
    path('api/login/', views.login_api, name='login_api'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('api/cart/add/<int:product_id>/', views.add_to_cart_api, name='add_to_cart_api'),
    path('api/cart/update/<int:item_id>/', views.update_cart_item_api, name='update_cart_item_api'),
    path('api/cart/remove/<int:item_id>/', views.remove_from_cart_api, name='remove_from_cart_api'),
    path('api/order/create/', views.create_order_api, name='create_order_api'),
    path('account/', views.account_view, name='account'),
    path('api/order/delete/<int:order_id>/', views.delete_order_api, name='delete_order_api'),
    path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('about/', views.about_view, name='about'),
]

