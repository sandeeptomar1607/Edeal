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


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.FloatField()
    description = models.TextField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="uploads/product")

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
