from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # ==================== HOME & AUTHENTICATION ====================
    path('', views.index, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # ==================== DASHBOARD ====================
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # ==================== PRODUCTS ====================
    path('products/', views.products_list, name='products_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:product_id>/edit/', views.product_update, name='product_edit'),
    path('products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    
    # ==================== CATEGORIES ====================
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/create/', views.category_create, name='category_create'),
    
    # ==================== ORDERS ====================
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/create/', views.create_order_from_cart, name='create_order'),
    
    # ==================== CART ====================
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    
    # ==================== USER PROFILE ====================
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # ==================== API ENDPOINTS ====================
    path('api/cart/', views.api_cart_data, name='api_cart'),
    path('api/user/', views.api_user_info, name='api_user'),
    
    # ==================== LEGACY ROUTES ====================
    path('items/', views.listItems, name='items'),
]

