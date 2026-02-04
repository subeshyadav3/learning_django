from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from decimal import Decimal
from .models import Item


def index(request):
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('items')
    return render(request, 'login.html')


@login_required(login_url='login')
def listItems(request):
    items = Item.objects.all()
    cart = request.session.get('cart', {})
    total = sum(Decimal(i['price']) * i['qty'] for i in cart.values())

    return render(
        request,
        'index.html',
        {
            'items': items,
            'cart': cart,
            'total': total
        }
    )


@login_required(login_url='login')
def cart_view(request):
    cart = request.session.get('cart', {})

    if request.method == 'POST':
        item_id = str(request.POST.get('item_id'))
        item = Item.objects.get(id=item_id)

        if item_id in cart:
            cart[item_id]['qty'] += 1
        else:
            cart[item_id] = {
                'name': item.name,
                'price': str(item.price),
                'qty': 1
            }

        request.session['cart'] = cart

    total = sum(Decimal(i['price']) * i['qty'] for i in cart.values())
    return JsonResponse({'cart': cart, 'total': total})