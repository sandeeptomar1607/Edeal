from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from store.models import Coupon, Product


def cart_add(request):
    cart = Cart(request)
    id = request.GET.get("pid")
    product = Product.objects.get(id=id)
    cart.add(product=product)
    product_in_cart = len(cart.cart)
    return JsonResponse(
        data={
            "product_in_cart": product_in_cart,
            "message": "Product added successfully",
        },
        status=200,
    )


def item_clear(request):
    cart = Cart(request)
    id = request.GET.get("pid")
    product = Product.objects.get(id=id)
    cart.remove(product)
    product_in_cart = len(cart.cart)
    return JsonResponse(
        data={
            "product_in_cart": product_in_cart,
            "message": "Product added successfully",
        },
        status=200,
    )


def item_increment(request):
    cart = Cart(request)
    id = request.GET.get("pid")
    product = Product.objects.get(id=id)
    cart.add(product=product)
    item = cart.cart
    quantity = item.get(id).get("quantity")
    return JsonResponse(
        data={
            "price": product.price,
            "quantity": quantity,
            "total": quantity * product.price,
            "message": "Product incremented",
        },
        status=200,
    )


def item_decrement(request):
    cart = Cart(request)
    id = request.GET.get("pid")
    product = Product.objects.get(id=id)
    q = cart.cart.get(str(product.id))
    item = cart.cart

    if q.get("quantity") == 1:
        quantity = 0
        item_clear(request)

    else:

        cart.decrement(product=product)
        quantity = item.get(id).get("quantity")
    return JsonResponse(
        data={
            "price": product.price,
            "quantity": quantity,
            "total": quantity * product.price,
            "message": "Product incremented",
        },
        status=200,
    )


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


def cart_detail(request):
    cart = Cart(request)
    cart_amount = 0
    for product in cart.cart.values():
        quantity = int(product.get("quantity"))
        price = float(product.get("price"))
        cart_amount += price * quantity
    product_in_cart = len(cart.cart)
    coupons = Coupon.objects.all()
    context = {"product_in_cart": product_in_cart, "cart_amount": cart_amount, 'coupons': coupons}
    return render(request, "store/cart_details.html", context)
