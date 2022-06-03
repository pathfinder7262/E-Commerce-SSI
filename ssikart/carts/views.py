from django.shortcuts import render, redirect
from matplotlib import is_interactive
from store.models import Product
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key #check if you session key have or not
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  #get the product
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) #get the cart using cart id present in session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.ObjectDoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart')


def cart(request,total=0,quantity = 0,cart_item=None):
    TAX_PERCENT = 5
    Tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = cart_item.objects.filter(cart = cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (TAX_PERCENT *total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    contaxt = {
        'total': total,
        'quantity' : quantity,
        'cart_items' : cart_item,
        'tax' : Tax,
        'grand_total' : grand_total,
    }

    return render(request, 'carts/cart.html')

