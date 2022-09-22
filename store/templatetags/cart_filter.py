from django import template
from django.db.models import Q

from store.models import Wishlist

register = template.Library()


@register.filter(name="in_electronics")
def in_electronics(sub_category):
    
    if sub_category.category.name == 'Electronics':
        return True
    else:
        return False

@register.filter(name="in_Beauty")
def in_Beauty(sub_category):
    if sub_category.category.name == 'Beauty,Toy & More':
        return True
    else:
        return False


@register.filter(name="in_home")
def in_home(sub_category):
    if sub_category.category.name == 'Home':
        return True
    else:
        return False 

@register.filter(name="in_cart")
def in_cart(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False


@register.filter(name="cart_quantity")
def cart_quantity(cart):

    return len(cart)


@register.filter(name="in_wishlist")
def in_wishlist(product, user):
    wishlist = Wishlist.objects.filter(Q(user=user) & Q(product_id=product.id)).exists()
    if wishlist:
        return True
    return False


@register.filter(name="wishlist_quantity")
def wishlist_quantity(user):
    wishlist = Wishlist.objects.filter(user=user).count()
    return wishlist
