from django.urls import path
from .views import BlogView,BlogViewDetails


urlpatterns = [
    path('blogs/', BlogView.as_view(), name='blog-list'),
    path('blogs/<int:pk>/', BlogViewDetails.as_view(), name='blog-list')
]
