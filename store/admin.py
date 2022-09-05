from django.contrib import admin

from .models import (Address, Category, Order, OrderLine, Product, User,
                     Wishlist)

# Register your models here.
admin.site.register(User),
admin.site.register(Category),
admin.site.register(Product),
admin.site.register(Address),
admin.site.register(Order),
admin.site.register(OrderLine),
admin.site.register(Wishlist)
