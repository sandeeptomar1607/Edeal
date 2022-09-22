from itertools import product
from math import dist
from pyexpat import model
from unicodedata import category
from wsgiref.simple_server import demo_app
from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django.db import models

from .manager import UserManager

User = settings.AUTH_USER_MODEL

# Create your models here.


class User(AbstractUser):

    role = (
        ("vender", "vender"),
        ("customer", "customer"),
    )
    username = None
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20)
    role = models.CharField(max_length=15, choices=role)
    image = models.ImageField(upload_to="uploads/profile", default=None)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Category(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField(upload_to="uploads/category", default=None)

    def __str__(self):
        return f"{self.name}"


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    image = models.ImageField(upload_to="uploads/category", default=None)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=None)
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=30)
    price = models.FloatField()
    specifications = models.TextField(max_length=200, null=True, blank=True)
    brand = models.CharField(
        max_length=20, default=None, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="uploads/product")
    seller = models.CharField(
        max_length=30, default=None, null=True, blank=True)
    highlight1 = models.CharField(max_length=200, null=True, blank=True)
    highlight2 = models.CharField(max_length=200, null=True, blank=True)
    highlight3 = models.CharField(max_length=200, null=True, blank=True)
    highlight4 = models.CharField(max_length=200, null=True, blank=True)
    war_summary = models.CharField(
        max_length=50, default="1 Year Onsite Warranty", null=True, blank=True)
    war_service_type = models.CharField(
        max_length=50, default="Onsite", null=True, blank=True)
    covered_in = models.CharField(
        max_length=50, default="Manufacturing Defects", null=True, blank=True)
    not_covered_in = models.CharField(
        max_length=50, default="Physical Damage", null=True, blank=True)
    domestic_war = models.CharField(
        max_length=50, default="1 Year", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.IntegerField()
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zip_code = models.IntegerField()


class Order(models.Model):

    status = (
        ("pending", "pending"),
        ("success", "success"),
        ("failed", "failed"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=status, default="pending")
    date = models.DateTimeField()
    order_id = models.CharField(max_length=100, default=None, null=True)
    amount = models.FloatField()


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product}"


class Coupon(models.Model):
    coupon_type = (
        ('min', 'min'),
        ('bank', 'bank'),
        ('category', 'category'),
        ('sub_cat', 'sub_cat'),
        ('brand', 'brand'),
        ('product','product')
    )
    dis_type = (
        ('in_percentage', 'in_percentage'),
        ('in_rupees','in_rupees')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon_type = models.CharField(max_length=8, choices=coupon_type)
    min = models.IntegerField(default=None, null=True, blank=True)
    bank = models.CharField(max_length=45,default=None, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, null=True, blank=True)
    sub_cat = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default=None, null=True, blank=True)
    brand = models.CharField(max_length=20, default=None, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None, null=True, blank=True)
    coupon_code = models.CharField(max_length=6)
    discount_type = models.CharField(max_length=15, choices=dis_type)
    discount = models.IntegerField()
    upto = models.IntegerField(default=None, null=True, blank=True)
    description = models.CharField(max_length=50)
    valid_till = models.DateField(default=None)


    def __str__(self):
        return f"{self.coupon_code}"