from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Sum, Count
from decimal import Decimal
from datetime import datetime
import logging

from .models import Item, Product, Category, Order, OrderItem, UserProfile
from .forms import UserRegistrationForm, UserLoginForm, ProductForm, CategoryForm, UserProfileForm, OrderFilterForm

logger = logging.getLogger(__name__)


# ==================== HOME & AUTHENTICATION ====================

def index(request):
    """Home page view - redirects to login if not authenticated"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def register_view(request):
    """
    User Registration View
    - Handles GET (form display) and POST (form submission)
    - Uses Django forms for data validation and security
    - Creates User and UserProfile objects
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save()
            
            # Create user profile
            UserProfile.objects.create(user=user, role='customer')
            
            logger.info(f"New user registered: {user.username}")
            
            # Store success message in session
            request.session['registration_success'] = f"Welcome {user.username}! Please log in."
            return redirect('login')
        else:
            context = {'form': form, 'errors': form.errors}
            return render(request, 'register.html', context)
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """
    User Login View
    - Demonstrates request/response handling
    - Uses sessions to maintain user state
    - Implements 'remember me' functionality
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Handle "Remember Me" functionality
                if remember_me:
                    request.session.set_expiry(7 * 24 * 60 * 60)  # 7 days
                    request.session['remember'] = True
                else:
                    request.session.set_expiry(0)  # Browser session
                
                # Store login time in session
                request.session['login_time'] = datetime.now().isoformat()
                
                logger.info(f"User logged in: {username}")
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
                logger.warning(f"Failed login attempt for user: {username}")
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    """
    User Logout View
    - Clears session data
    - Removes authentication
    """
    user = request.user.username
    logout(request)
    logger.info(f"User logged out: {user}")
    return redirect('login')


# ==================== DASHBOARD & PRODUCT VIEWS ====================

@login_required(login_url='login')
def dashboard(request):
    """
    User Dashboard
    - Shows personalized content based on user role
    - Demonstrates authorization checks
    """
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, role='customer')
    
    # Get statistics
    total_orders = Order.objects.filter(user=request.user).count()
    total_spent = Order.objects.filter(user=request.user).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    context = {
        'profile': profile,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'recent_orders': Order.objects.filter(user=request.user).order_by('-created_at')[:5],
    }
    
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def products_list(request):
    """
    Product List View
    - Demonstrates CRUD Read operation
    - Shows filter and search functionality
    - Implements pagination-like behavior
    """
    products = Product.objects.all().select_related('category')
    categories = Category.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Filter by category
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        products = products.filter(status=status)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    products = products.order_by(sort_by)
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_status': status,
    }
    
    return render(request, 'products_list.html', context)


@login_required(login_url='login')
def product_detail(request, product_id):
    """
    Product Detail View
    - Shows single product details
    - Demonstrates one-to-many relationships
    """
    product = get_object_or_404(Product, id=product_id)
    
    context = {
        'product': product,
        'category': product.category,
    }
    
    return render(request, 'product_detail.html', context)


def is_staff(user):
    """Check if user is staff member"""
    try:
        return user.profile.role in ['staff', 'admin']
    except UserProfile.DoesNotExist:
        return False


@login_required(login_url='login')
@user_passes_test(is_staff, login_url='dashboard')
def product_create(request):
    """
    Create Product View
    - Demonstrates CRUD Create operation
    - Restricted to staff users (Authorization)
    - Handles form POST data
    """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            
            logger.info(f"Product created by {request.user.username}: {product.name}")
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm()
    
    context = {'form': form, 'title': 'Create Product'}
    return render(request, 'product_form.html', context)


@login_required(login_url='login')
@user_passes_test(is_staff, login_url='dashboard')
def product_update(request, product_id):
    """
    Update Product View
    - Demonstrates CRUD Update operation
    - Restricted to staff users
    """
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            logger.info(f"Product updated by {request.user.username}: {product.name}")
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'title': 'Update Product', 'product': product}
    return render(request, 'product_form.html', context)


@login_required(login_url='login')
@user_passes_test(is_staff, login_url='dashboard')
@require_http_methods(["POST"])
def product_delete(request, product_id):
    """
    Delete Product View
    - Demonstrates CRUD Delete operation
    - Only accepts POST requests
    - Restricted to staff users
    """
    product = get_object_or_404(Product, id=product_id)
    product_name = product.name
    product.delete()
    
    logger.info(f"Product deleted by {request.user.username}: {product_name}")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'deleted', 'message': f'Product {product_name} deleted successfully'})
    
    return redirect('products_list')


# ==================== CATEGORY VIEWS ====================

@login_required(login_url='login')
def categories_list(request):
    """List all categories"""
    categories = Category.objects.annotate(product_count=Count('products'))
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'categories_list.html', context)


@login_required(login_url='login')
@user_passes_test(is_staff, login_url='dashboard')
def category_create(request):
    """Create new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            logger.info(f"Category created by {request.user.username}: {category.name}")
            return redirect('categories_list')
    else:
        form = CategoryForm()
    
    return render(request, 'category_form.html', {'form': form})


# ==================== ORDER VIEWS ====================

@login_required(login_url='login')
def orders_list(request):
    """
    Orders List View
    - Shows all orders for authenticated user
    - Demonstrates filtering and ordering
    - Shows many-to-one relationships
    """
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    
    form = OrderFilterForm(request.GET)
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        orders = orders.filter(status=status)
    
    # Sort orders
    sort_by = request.GET.get('sort_by', '-created_at')
    if sort_by == 'newest':
        orders = orders.order_by('-created_at')
    elif sort_by == 'oldest':
        orders = orders.order_by('created_at')
    elif sort_by == 'price_high':
        orders = orders.order_by('-total_amount')
    elif sort_by == 'price_low':
        orders = orders.order_by('total_amount')
    
    context = {
        'orders': orders,
        'form': form,
    }
    
    return render(request, 'orders_list.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    """
    Order Detail View
    - Shows detailed order information
    - Demonstrates many-to-many through relationships (Order -> OrderItem -> Product)
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all().select_related('product')
    
    context = {
        'order': order,
        'items': items,
    }
    
    return render(request, 'order_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def create_order_from_cart(request):
    """
    Create Order from Cart
    - Demonstrates conversion of session cart to database records
    - CRUD Create for multiple related models
    """
    cart = request.session.get('cart', {})
    
    if not cart:
        return JsonResponse({'status': 'error', 'message': 'Cart is empty'}, status=400)
    
    try:
        # Create order
        total_amount = sum(Decimal(item['price']) * item['qty'] for item in cart.values())
        order = Order.objects.create(user=request.user, total_amount=total_amount)
        
        # Create order items
        for item_id, item_data in cart.items():
            product = Product.objects.get(id=int(item_id))
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['qty'],
                price_at_purchase=Decimal(item_data['price'])
            )
        
        # Clear cart session
        request.session['cart'] = {}
        request.session.modified = True
        
        logger.info(f"Order created for {request.user.username}: Order #{order.id}")
        
        return JsonResponse({
            'status': 'success',
            'message': f'Order created successfully. Order ID: {order.id}',
            'order_id': order.id
        })
    
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Error creating order'}, status=500)


# ==================== CART VIEWS ====================

@login_required(login_url='login')
def cart_view(request):
    """
    Shopping Cart View
    - Demonstrates session handling
    - Shows add/update/delete cart functionality
    - Uses AJAX for dynamic updates
    """
    if request.method == 'GET':
        cart = request.session.get('cart', {})
        total = sum(Decimal(item['price']) * item['qty'] for item in cart.values())
        
        return render(request, 'cart.html', {'cart': cart, 'total': total})
    
    return redirect('products_list')


@login_required(login_url='login')
@require_http_methods(["POST"])
def add_to_cart(request):
    """
    Add item to cart (AJAX endpoint)
    - Demonstrates form data handling via POST
    - Manages session data
    - Returns JSON response
    """
    try:
        item_id = str(request.POST.get('item_id'))
        quantity = int(request.POST.get('quantity', 1))
        
        product = Product.objects.get(id=item_id)
        
        cart = request.session.get('cart', {})
        
        if item_id in cart:
            cart[item_id]['qty'] += quantity
        else:
            cart[item_id] = {
                'name': product.name,
                'price': str(product.price),
                'qty': quantity,
                'image_url': product.image_url or ''
            }
        
        request.session['cart'] = cart
        request.session.modified = True
        
        total = sum(Decimal(item['price']) * item['qty'] for item in cart.values())
        
        logger.info(f"Item added to cart by {request.user.username}: {product.name}")
        
        return JsonResponse({
            'status': 'success',
            'message': f'{product.name} added to cart',
            'cart': cart,
            'total': str(total),
            'cart_count': len(cart)
        })
    
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
    except Exception as e:
        logger.error(f"Error adding to cart: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Error adding to cart'}, status=500)


@login_required(login_url='login')
@require_http_methods(["POST"])
def remove_from_cart(request):
    """Remove item from cart"""
    try:
        item_id = str(request.POST.get('item_id'))
        cart = request.session.get('cart', {})
        
        if item_id in cart:
            removed_item = cart.pop(item_id)
            request.session['cart'] = cart
            request.session.modified = True
            
            total = sum(Decimal(item['price']) * item['qty'] for item in cart.values())
            
            return JsonResponse({
                'status': 'success',
                'message': f'{removed_item["name"]} removed from cart',
                'cart': cart,
                'total': str(total)
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'Item not found in cart'}, status=404)
    
    except Exception as e:
        logger.error(f"Error removing from cart: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Error removing from cart'}, status=500)


# ==================== USER PROFILE VIEWS ====================

@login_required(login_url='login')
def profile_view(request):
    """
    User Profile View
    - Demonstrates one-to-one relationships
    - Shows user's profile information
    """
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, role='customer')
    
    context = {
        'profile': profile,
        'user': request.user,
    }
    
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def profile_edit(request):
    """
    Edit User Profile
    - Demonstrates form handling for model instances
    """
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, role='customer')
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            logger.info(f"Profile updated for user: {request.user.username}")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {'form': form}
    return render(request, 'profile_edit.html', context)


# ==================== API ENDPOINTS ====================

@login_required(login_url='login')
def api_cart_data(request):
    """API endpoint to get cart data as JSON"""
    cart = request.session.get('cart', {})
    total = sum(Decimal(item['price']) * item['qty'] for item in cart.values())
    
    return JsonResponse({
        'cart': cart,
        'total': str(total),
        'item_count': len(cart)
    })


@login_required(login_url='login')
def api_user_info(request):
    """API endpoint to get user information as JSON"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = None
    
    return JsonResponse({
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'is_authenticated': request.user.is_authenticated,
        'profile': {
            'role': profile.role if profile else 'customer',
            'phone': profile.phone if profile else '',
            'city': profile.city if profile else '',
        } if profile else None,
        'login_time': request.session.get('login_time', '')
    })


# List items (legacy view for backward compatibility)
@login_required(login_url='login')
def listItems(request):
    """Legacy view - redirects to products list"""
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'index.html', context)
