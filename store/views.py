import datetime
import json

import pytz
import razorpay
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from edeal import settings

from .cart import *
from .forms import SignupForm
from .models import Address, Category, Order, OrderLine, Product, User, Wishlist

IST = pytz.timezone("Asia/Kolkata")

# Create your views here.


class Home(View):
    """
    Home Page: Shows all products.
    """

    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.all()
        form = SignupForm()

        context = {"categories": categories, "products": products, "form": form}

        return render(request, "store/home.html", context)


class venderHome(View):
    """
    Vender Home Page : This page shows all products of authenticated Vender.
    """

    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.filter(user=request.user)
        context = {"products": products, "categories": categories}
        return render(request, "store/venderHome.html", context)


class SignUp(View):
    """
    SignUP: User can register on E-Deal by these view.
    """

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            message = "you have successfully registered with E-Deal."
            return JsonResponse({"message": message}, status=200)
        else:
            return JsonResponse(status=400)


class LoginView(View):
    """
    LogIn: User can LogIn to the E-Deal by these view. After successfully Logged In, user will redirected to the Customer home page or Vender home page based on their registered role.
    """

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            if user.role == "vender":
                return redirect("store:venderHome")

            if user.role == "customer":
                # import pdb;pdb.set_trace()
                return redirect("store:home")

        else:
            return redirect("store:login")


def userLogout(request):
    """
    LogOut View: User will Logged Out.

    """
    logout(request)
    return redirect("store:home")


class AddProduct(LoginRequiredMixin, View):

    login_url = settings.login_url

    """
    AddProduct View: Vender can add their prodcut on E-Deal.

    """

    def post(self, request):
        cat_id = request.POST.get("category")
        category = Category.objects.get(id=cat_id)
        name = request.POST.get("name")
        price = request.POST.get("price")
        desc = request.POST.get("desc")
        image = request.FILES.get("p-image")
        product = Product.objects.create(
            user=request.user,
            category=category,
            name=name,
            price=price,
            description=desc,
            image=image,
        )

        if product:
            message = "Product added successfully."
            prodcut_data = User.objects.values()
            return JsonResponse({"student_data": list(prodcut_data)}, status=200)
        else:
            return JsonResponse({"message": "failed"}, status=400)


class DeleteProduct(LoginRequiredMixin, View):

    login_url = settings.login_url

    """
    Delete Product View: Vender can delete their products from E-Deal.

    """

    def post(self, request):
        id = request.POST.get("pid")
        product = Product.objects.get(pk=id)
        product.delete()
        return JsonResponse(data={"message": "Data deleted successfully"}, status=200)


" Razorpay client object"
client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))


class PaymentView(View):
    """
    Payment View: When a Customer make a payment, their address will be saved. An order will be created and redirect to Rajorpay payment.
    """

    def post(self, request):
        mobile = request.POST.get("mobile")
        adrs = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip = request.POST.get("zip_code")
        user = request.user

        address = Address.objects.create(
            user=user, mobile=mobile, address=adrs, city=city, state=state, zip_code=zip
        )

        cart = Cart(request)
        today = datetime.datetime.now(IST)
        final_price = 0
        order = Order.objects.create(user=user, date=today, amount=final_price)
        all_orderlines = []
        for product in cart.cart.values():
            quantity = int(product.get("quantity"))
            price = float(product.get("price"))
            product = int(product.get("product_id"))

            all_orderlines.append(
                OrderLine(user=user, order=order, product_id=product, quantity=quantity)
            )
            final_price += price * quantity
        orderline = OrderLine.objects.bulk_create(all_orderlines)

        order.amount = final_price
        callback_url = "http://" + str(get_current_site(request)) + "/handlerequest/"
        razorpay_order = client.order.create(
            dict(
                amount=final_price * 100,
                currency=settings.order_currency,
                payment_capture="1",
            )
        )

        order.order_id = razorpay_order["id"]
        order.save()
        cart.clear()
        orderlines = OrderLine.objects.filter(order=order)
        context = {
            "order": order,
            "order_id": razorpay_order["id"],
            "final_price": final_price,
            "razorpay_merchant_id": settings.razorpay_id,
            "callback_url": callback_url,
            "orderlines": orderlines,
            "address": address,
        }
        return render(request, "store/paymentsummary.html", context)


@csrf_exempt
def handlerequest(request):
    """
    Handle Request: Handles the request send by Rajorpay payment. These view verify the request and will redirect to the success or failed page according to the verification status.
    """
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id", "")
        order_id = request.POST.get("razorpay_order_id", "")
        signature = request.POST.get("razorpay_signature", "")

        params_dict = {
            "razorpay_payment_id": payment_id,
            "razorpay_order_id": order_id,
            "razorpay_signature": signature,
        }

        order_db = Order.objects.get(order_id=order_id)
        try:
            check = client.utility.verify_payment_signature(params_dict)
            order_db.status = "success"
            order_db.save()
            return render(request, "store/success.html")

        except:
            order_db.status = "failed"
            order_db.save()
            return render(request, "store/failed.html")


class OrderView(View):
    # login_url = settings.login_url
    """
    Order View: Shows all order of the authenticated Customer.
    """

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        result = {}
        for order in orders:
            orderlines = OrderLine.objects.filter(order=order)
            result[order] = orderlines

        context = {"result": result, "orders": orders}
        return render(request, "store/order.html", context)


class AddToWishlist(View):
    """
    Add to wishlist View: Add Products to customer's wishlist.
    """

    def get(self, request):
        product_id = request.GET.get("pid")
        Wishlist.objects.create(user=request.user, product_id=product_id)
        in_wishlist = Wishlist.objects.filter(user=request.user).count()
        return JsonResponse(
            data={"message": "Added successfully", "in_wishlist": in_wishlist},
            status=200,
        )


class RemoveFromWishlist(View):
    """
    Remove Products: Remove products from the customer's wihslist.
    """

    def get(self, request):
        id = request.GET.get("pid")
        wishlist = Wishlist.objects.filter(Q(user=request.user) & Q(product_id=id))
        wishlist.delete()
        # Wishlist.objects.get(product_id=id).delete()
        in_wishlist = Wishlist.objects.filter(user=request.user).count()
        return JsonResponse(
            data={"message": "Data deleted successfully", "in_wishlist": in_wishlist},
            status=200,
        )


class WishlistView(LoginRequiredMixin, View):
    login_url = settings.login_url

    """
    Wishlist: Shows all products which are added to the customer's wishlist.
    """

    def get(self, request):
        wishlists = Wishlist.objects.filter(user=request.user)
        context = {"wishlists": wishlists}
        return render(request, "store/wishlist.html", context)


class UpdateProduct(View):
    # def get(self,request,pk=None):
    def get(self, request):

        id = request.GET.get("pid")
        product = Product.objects.get(pk=id)
        print("================", product.price)

        # return render(request,'store/venderHome.html',{'product': product, 'msg':"success"})

        # class UpdateProduct(View):
        #     def post(self, request):
        #         id = request.POST.get('pid')
        #         product = Product.objects.get(pk=id)
        #         # import pdb; pdb.set_trace()

        #         image = json.dumps(str(product.image))

        product_data = {
            "id": product.id,
            "category": product.category.name,
            "name": product.name,
            "price": product.price,
            "description": product.description,
        }

        return JsonResponse(product_data)