from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('product_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


@login_required(login_url='login')
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('product_list')

@login_required(login_url='login')
def view_cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0
    for pid, qty in cart.items():
        try:
            product = Product.objects.get(id=pid)
            product.qty = qty
            product.total_price = qty * product.price
            total += product.total_price
            products.append(product)
        except Product.DoesNotExist:
            continue
    return render(request, 'cart.html', {'products': products, 'total': total})
