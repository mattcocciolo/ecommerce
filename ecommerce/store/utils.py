import json

from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode

from .models import *
from .tokens import account_activation_token


def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.customer.email_confirmed = True
        user.save()
        login(request, user)
        customer = user.customer
        email = customer.email
        welcome_email(email, customer)

        return render(request, 'store/account_activation_finish.html')
    else:
        return render(request, 'store/account_activation_invalid.html')


def welcome_email(email, customer):
    # Envia un mail de bienvenida al finalizar activacion del usuario
    email_subject = 'Gracias por registrarte en SHOP'
    message = f'Felicitaciones {customer}, tu usuario, fue activado con exito. ' \
              f'\nTe damos la bienvenida a SHOP, tu sitio de compras online. No pares de Comprar!!!' \
              f'\n\n\nHave lot of fun!!!' \
              f'\nShop WebMaster Team'
    to_email = email
    email = EmailMessage(email_subject, message, to=[to_email])
    email.send()


def cookiecart(request):
    # Crear carro vacío por ahora para usuarios no registrados
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartitems = order['get_cart_items']

    for i in cart:
        # Usamos el bloque de prueba para evitar que los artículos en el carrito
        # que pueden haberse eliminado causen errores
        try:
            cartitems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image_url,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
            if not product.digital:
                order['shipping'] = True
        except:
            pass

    return {'cartitems': cartitems, 'order': order, 'items': items}


def cartdata(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        cookiedata = cookiecart(request)
        cartitems = cookiedata['cartitems']
        order = cookiedata['order']
        items = cookiedata['items']

    return {'cartitems': cartitems, 'order': order, 'items': items}


def guest_order(request, data):
    print('Usuario no Logueado')
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    cookiedata = cookiecart(request)
    items = cookiedata['items']
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()
    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderitem = OrderItem.objects.create(product=product, order=order, quantity=item['quantity'])

    return customer, order
