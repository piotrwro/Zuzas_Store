from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

# Create your views here.
from cart.cart import Cart
from cart.forms import CartAddProductForm
from zuzas_store.models import Product, CartOrderProduct, CartOrder, UserProfile


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})

    return render(request, 'cart/detail.html', context={'cart': cart})


def order_create(request):
    user = request.user
    cart = Cart(request)
    if not request.user.is_authenticated:
        if request.method == 'POST':
            total_price = cart.get_total_price()
            cart_order = CartOrder.objects.create(total_price=total_price)
            for item in cart:
                CartOrderProduct.objects.create(cart_order=cart_order,
                                                product=item['product'],
                                                price=item['price'],
                                                quantity=item['quantity'])

            cart.clear()
            return render(request, 'order/created.html', context={'cart_order': cart_order})

        else:

            return render(request, 'order/create.html', {'cart': cart})

    else:

        if request.method == 'POST':
            user_profile = UserProfile.objects.get(user=user)
            total_price = cart.get_total_price()
            cart_order = CartOrder.objects.create(user=user_profile, total_price=total_price)
            for item in cart:
                CartOrderProduct.objects.create(cart_order=cart_order,
                                                product=item['product'],
                                                price=item['price'],
                                                quantity=item['quantity'])

            cart.clear()
            return render(request, 'order/created.html',  context={'cart_order': cart_order})

        else:

            return render(request, 'order/create.html', {'cart': cart})
