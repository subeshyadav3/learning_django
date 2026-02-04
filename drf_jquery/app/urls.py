from django.urls import path
from .views import index, listItems, login_view, register_view, cart_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('', index, name='home'),
    path('items/', listItems, name='items'),
    path('cart/', cart_view),
]
