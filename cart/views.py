from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) #get the product
    try :
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product,user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))#get the cart using the cart_id present in the session
            cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user=request.user
            )
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
        
        cart_item.save()
    except Cart.DoesNotExist:
        # Create the cart if it does not exist
        cart = Cart.objects.create(cart_id=_cart_id(request))
        if request.user.is_authenticated:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=request.user
            )
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
        cart_item.save()
    return redirect('cart')

def remove_cart(request,product_id):
    
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request,product_id):
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0,quantity=0,cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = (0.5*total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total': grand_total,
    }
    return render(request,'store/cart.html',context)
@login_required(login_url='login')
def checkout(request, total=0,quantity=0,cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = (0.5*total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html',context)

def proceed_to_pay(request):
    # Assuming the user is logged in and has an order
    user = request.user
    order = Order.objects.filter(user=user, is_ordered=False).first()

    if not order or not order.delivery_address:
        messages.error(request, "Please fill your delivery address before proceeding to payment.")
        return redirect("checkout")  # Redirect back to checkout page

    # Proceed to payment if address exists
    return redirect("payments")  # Replace with your actual payment URL