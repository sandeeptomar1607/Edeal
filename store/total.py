from cart.cart import Cart

from .models import Product


def total(request):
    cart = Cart(request)
    # today = datetime.datetime.now(IST)
    final_price = 0
    for product in cart.cart.values():
        quantity = int(product.get("quantity"))
        price = float(product.get("price"))
        final_price += price * quantity
    return final_price


def pro_category(request, cat):
    cart = Cart(request)
    discounted_amount = 0

    for product in cart.cart.values():
        product_id = int(product.get("product_id"))
        try:
            product = Product.objects.get(id=product_id, category=cat)
            discounted_amount += product.price

        except:
            pass

    return discounted_amount


def pro_sub_category(request, sub_cat):
    cart = Cart(request)
    discounted_amount = 0

    for product in cart.cart.values():
        product_id = int(product.get("product_id"))
        try:
            product = Product.objects.get(id=product_id, sub_category=sub_cat)
            discounted_amount += product.price

        except:
            pass

    return discounted_amount


def pro_brand(request, brand):
    cart = Cart(request)
    discounted_amount = 0

    for product in cart.cart.values():
        product_id = int(product.get("product_id"))
        try:
            product = Product.objects.get(id=product_id, brand=brand)
            discounted_amount += product.price

        except:
            pass
    return discounted_amount


def prod(request, pro):
    cart = Cart(request)
    discounted_amount = 0
    for product in cart.cart.values():
        product_id = int(product.get("product_id"))
        try:
            product = Product.objects.get(id=product_id)
            if product == pro:
                discounted_amount = product.price
        except:
            pass

    return discounted_amount




git remote set-url origin https://sandeeptomar1607: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@github.com/sandeeptomar1607/git@github.com:sandeeptomar1607/Edeal.git