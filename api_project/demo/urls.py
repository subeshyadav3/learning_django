from django.urls import path
from demo import views
urlpatterns = [
    path("",views.home,name="home"),
    path('product/list/',views.ProductList.as_view(),name='product-list'),
    path('product/<int:id>/',views.ProductDetail.as_view(),name='product-detail'),
]