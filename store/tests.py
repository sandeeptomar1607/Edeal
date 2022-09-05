import datetime
import io

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from PIL import Image

from .models import Category, Order, Product, User, Wishlist

" Creates a test image "
client = Client()


def create_image(
    storage, filename, size=(100, 100), image_mode="RGB", image_format="PNG"
):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = io.BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


# Create your tests here.


class LoginTest(TestCase):
    def setUp(self):
        self.vender = {
            "email": "vender@gmail.com",
            "password": "secret",
            "role": "vender",
        }
        self.customer = {
            "email": "cutomer@gmail.com",
            "password": "secret",
            "role": "customer",
        }

        User.objects.create_user(**self.vender)
        User.objects.create_user(**self.customer)

    def test_login_with_vender(self):
        response = self.client.post("/login/", self.vender, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/venderHome/")

    def test_login_with_customer(self):
        response = self.client.post("/login/", self.customer, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/")


class AddProductTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        vender = User.objects.create_user(
            email="test@gmail.com", password="password", role="vender"
        )
        category = Category.objects.create(name="mens")

        image = create_image(None, "avatar.png")
        image_file = SimpleUploadedFile("front.png", image.getvalue())
        cls.data = {
            "user": vender,
            "name": "watch",
            "category": category.id,
            "image": image_file,
            "price": 23,
        }

    def test_redirect_if_not_logged_in(self):
        response = self.client.post("/addproduct/")
        self.assertRedirects(response, "/?next=/addproduct/")

    def test_add_product_view_if_logged_in(self):

        self.client.login(email="test@gmail.com", password="password")

        response = self.client.post("/addproduct/", self.data)

        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(response.status_code, 200)


class DeleteProductTest(TestCase):
    def setUp(self):
        vender = User.objects.create_user(
            email="test@gmail.com", password="password", role="vender"
        )

        category = Category.objects.create(name="men's")

        self.product1 = Product.objects.create(
            user=vender, name="watch", category=category, image="test.jpg", price=23
        )

        self.product2 = Product.objects.create(
            user=vender, name="watch", category=category, image="test.jpg", price=23
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.post("/deleteproduct/", {"pid": self.product1.pk})
        self.assertRedirects(response, "/?next=/deleteproduct/")

    def test_delete_product_view_if_logged_in(self):
        self.client.login(email="test@gmail.com", password="password")
        response = self.client.post("/deleteproduct/", {"pid": self.product1.pk})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)


class AddToCartTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email="test@gmail.com", password="password", role="customer"
        )

        category = Category.objects.create(name="men's")

        self.product = Product.objects.create(
            user=user, name="watch", category=category, image="try.jpg", price=23
        )

        self.data = {
            "user": user,
            "mobile": "1111111111",
            "address": "Indore",
            "city": "indore",
            "state": "MP",
            "zip_code": "111111",
        }

    def test_add_to_cart_if_logged_in(self):
        self.client.login(email="test@gmail.com", password="password")

        response = self.client.get("/add/", {"pid": self.product.pk})
        self.assertEqual(response.status_code, 200)

        # Test payment view
        response = self.client.post(reverse("store:payment"), self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)


class AddToWishlistTest(TestCase):
    def setUp(self):
        customer = User.objects.create_user(
            email="test@gmail.com", password="password", role="cutomer"
        )

        category = Category.objects.create(name="men's")

        self.product = Product.objects.create(
            user=customer, name="watch", category=category, image="test.jpg", price=23
        )

    def test_add_to_wishlist_view(self):
        self.client.login(email="test@gmail.com", password="password")
        response = self.client.get("/wishlist/", {"pid": self.product.pk})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Wishlist.objects.count(), 1)


class RemoveFromWishlistTest(TestCase):
    def setUp(self):
        customer = User.objects.create_user(
            email="test@gmail.com", password="password", role="cutomer"
        )

        category = Category.objects.create(name="men's")

        self.product1 = Product.objects.create(
            user=customer, name="watch", category=category, image="test.jpg", price=23
        )

        self.product2 = Product.objects.create(
            user=customer, name="shirt", category=category, image="test.jpg", price=23
        )

        Wishlist.objects.create(user=customer, product=self.product1)
        Wishlist.objects.create(user=customer, product=self.product2)

    def test_add_to_wishlist_view(self):
        self.client.login(email="test@gmail.com", password="password")
        response = self.client.get("/remove-from-wishlist/", {"pid": self.product1.pk})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Wishlist.objects.count(), 1)
