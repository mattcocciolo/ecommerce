from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from store.models import Order, OrderItem, ShippingAddress

from .decorators import allowed_users


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employees'])
def ware(request):
    return render(request, 'ware/ware.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employees'])
def orders(request):
    order = Order.objects.all()
    context = {'orders': order}
    return render(request, 'ware/orders.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employees'])
def process_orders(request, pk_transaction_id):
    order = Order.objects.filter(transaction_id=pk_transaction_id)
    item = OrderItem.objects.filter()
    ship = ShippingAddress.objects.all()
    context = {'orders': order, 'items': item, 'ships': ship}
    return render(request, 'ware/process_orders.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employees', 'customers'])
def processed_orders(request):
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
        print(group)

    order = Order.objects.all()
    context = {'orders': order, 'group': group}
    return render(request, 'ware/processed_orders.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employees', 'customers'])
def details(request, pk_transaction_id):
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
        print(group)

    order = Order.objects.filter(transaction_id=pk_transaction_id)
    item = OrderItem.objects.filter()
    ship = ShippingAddress.objects.all()
    context = {'orders': order, 'items': item, 'ships': ship, 'group': group}
    return render(request, 'ware/details.html', context)


def button_id(request, pk_transaction_id):
    if request.method == "GET":
        order = Order.objects.get(transaction_id=pk_transaction_id)
        order.transaction_id = pk_transaction_id
        order.processed = True
        order.save()
        print(order.processed)
        print(order.transaction_id)
    return redirect('orders')
