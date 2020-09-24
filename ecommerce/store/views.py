import datetime
import json

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from ware.decorators import unauthenticated_user, allowed_users

from .forms import CreateUserForm, CustomerForm, ShippingForm
from .models import *
from .tokens import account_activation_token
from .utils import cartdata, guest_order


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activar Tu Cuenta de Usuario de Shop'
            message = render_to_string('store/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            user = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            customer, created = Customer.objects.get_or_create(email=email)
            new_user = form.save()
            customer.user = new_user
            customer.name = user
            group = Group.objects.get(name='customers')
            new_user.groups.add(group)
            customer.email = email
            customer.save()
            return render(request, 'store/account_activation_sent.html')
    context = {'form': form}
    return render(request, 'store/register.html', context)


def account_activation_sent(request):
    return render(request, 'store/account_activation_sent.html')


def account_activation_invalid(request):
    return render(request, 'store/account_activation_invalid.html')


def account_activation_finish(request):
    return render(request, 'store/account_activation_finish.html')


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group == 'customers':
                    return redirect('store')
                else:
                    return redirect('ware')
        else:
            messages.info(request, 'Nombre de Usuario o Password Incorrecto')
    context = {}
    return render(request, 'store/login.html', context)


def logout_user(request):
    group = request.user.groups.all()[0].name
    print(group)
    if group == 'customers':
        logout(request)
        return redirect('store')
    else:
        logout(request)
        return redirect('ware')


def store(request):
    data = cartdata(request)
    cartitems = data['cartitems']
    products = Product.objects.all()
    context = {'products': products, 'cartitems': cartitems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartdata(request)
    cartitems = data['cartitems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartitems': cartitems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartdata(request)
    cartitems = data['cartitems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartitems': cartitems}
    return render(request, 'store/checkout.html', context)


def updateitem(request):
    data = json.loads(request.body)
    productid = data['productid']
    action = data['action']
    print('productid:', productid)
    print('action:', action)
    customer = request.user.customer
    product = Product.objects.get(id=productid)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)
    orderitem.save()
    if orderitem.quantity <= 0:
        orderitem.delete()
    return JsonResponse('Articulo Agregado', safe=False)


def processorder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse('Pago Enviado...', safe=False)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def set_profile(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    data = cartdata(request)
    cartitems = data['cartitems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartitems': cartitems, 'form': form}
    return render(request, 'store/set_profile.html', context)


def profile_ship(request):
    customer = request.user.customer
    ship, create = ShippingAddress.objects.get_or_create(customer=customer)
    if request.method == "POST":
        form = ShippingForm(request.POST, instance=ship)
        if form.is_valid():
            ship.save()
            return redirect('set_profile')
    else:
        form = ShippingForm(instance=ship)
    data = cartdata(request)
    cartitems = data['cartitems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartitems': cartitems, 'form': form}
    return render(request, 'store/profile_ship.html', context)


def profile_orders(request):
    order_profile = Order.objects.all()
    data = cartdata(request)
    cartitems = data['cartitems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartitems': cartitems, 'orders_profiles': order_profile}
    return render(request, 'store/profile_orders.html', context)


def profile_passwd_update(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Tu Contraseña se actualizo exitosamente!')
            return redirect('profile_passwd_update')
        else:
            messages.error(request, 'Las contraseñas no coinciden, por favor, corrija el error!')
    else:
        form = PasswordChangeForm(request.user)

    data = cartdata(request)
    cartitems = data['cartitems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartitems': cartitems, 'form': form}
    return render(request, 'store/profile_passwd_update.html', context)


def product_details(request, pk_id):
    products = Product.objects.filter(id=pk_id)
    photos = ProductImages.objects.filter(product_id=pk_id)

    data = cartdata(request)
    cartitems = data['cartitems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartitems': cartitems, 'products': products, 'photos': photos}
    return render(request, 'store/product_details.html', context)
