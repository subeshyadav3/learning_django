# api/urls.py
from django.urls import path
from .views import ItemListCreateAPIView, ItemDetailAPIView, index

urlpatterns = [
    path('', index, name='home'),
    path('items/', ItemListCreateAPIView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemDetailAPIView.as_view(), name='item-detail'),
]
