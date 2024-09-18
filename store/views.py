from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from . models import Product, ReviewRating
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from . forms import ReviewForm
from orders.models import OrderProduct
# from django.http import HttpResponse
# Create your views here.
def store(request, category_slug=None):
    categories = None
    products =  None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category = categories, is_available=True)
    else:

        products = Product.objects.all().filter(is_available=True)
        
    context = {
        'products': products,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product = single_product).exists()
        
        
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user = request.user, product_id = single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
    # get the reviews 
    reviews = ReviewRating.objects.filter(product_id = single_product.id, status = True)

    context = {
        'single_product': single_product,
        'in_cart' : in_cart,
        'orderproduct' : orderproduct,
        'reviews' : reviews,
    }
    return render(request,'store/product_detail.html',context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id = request.user.id, product__id = product_id)
            form = ReviewForm(request.POST, instance = reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)