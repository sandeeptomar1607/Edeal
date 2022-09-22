import datetime

import pytz
import razorpay
from django.contrib import messages
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
from .models import (
    Address,
    Category,
    Coupon,
    Order,
    OrderLine,
    Product,
    SubCategory,
    User,
    Wishlist,
)
from .total import *

IST = pytz.timezone("Asia/Kolkata")

# Create your views here.
class CustomLoginRequiredMixin(LoginRequiredMixin):

    permission_denied_message = "You have to be logged in to access that page"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.WARNING, self.permission_denied_message
            )
            return self.handle_no_permission()
        return super(CustomLoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class Home(View):
    """
    Home Page: Shows all products.
    """

    def get(self, request):
        cat_id = request.GET.get("category")
        sub_cat_id = request.GET.get("sub_cat")

        categories = Category.objects.all()
        products = Product.objects.all()
        sub_categories = SubCategory.objects.all()
        form = SignupForm()

        if cat_id:
            category = Category.objects.get(id=cat_id)
            products = Product.objects.filter(category=category)
            context = {"category": category, "products": products}
            return render(request, "store/category1.html", context)
        elif sub_cat_id:
            sub_cat = SubCategory.objects.get(id=sub_cat_id)
            products = Product.objects.filter(sub_category=sub_cat)
            brands = []
            for p in products:
                if p.brand not in brands:
                    brands.append(p.brand)
            context = {"products": products, "brands": brands}
            return render(request, "store/category1.html", context)

        context = {
            "categories": categories,
            "sub_categories": sub_categories,
            "products": products,
            "form": form,
        }
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
            return JsonResponse(data={"role": user.role}, status=200)

        else:
            message = "Email or Password is incorrect."
            return JsonResponse(data={"message": message}, status=400)


class Profile(CustomLoginRequiredMixin, View):
    login_url = settings.login_url
    permission_denied_message = "Please login to view your profile"

    def get(self, request):
        return render(request, "store/profile.html")

    def post(self, request):
        user = request.user
        l_name = request.POST.get("last_name")
        f_name = request.POST.get("first_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        if f_name or l_name:
            user.first_name = f_name
            user.last_name = l_name

        if email:
            user.email = email

        if mobile:

            user.mobile = mobile
        user.save()

        if user:
            message = "Product added successfully."

            return JsonResponse(
                data={
                    "f_name": request.user.first_name,
                    "l_name": request.user.last_name,
                },
                status=200,
            )
        else:
            return JsonResponse({"message": "failed"}, status=400)


def userLogout(request):
    """
    LogOut View: User will Logged Out.

    """
    logout(request)
    return redirect("store:home")


class ProductDetail(View):
    def get(self, request, pk=None):
        product = Product.objects.get(id=pk)
        context = {"product": product}
        return render(request, "store/product.html", context)


class AddProduct(CustomLoginRequiredMixin, View):

    login_url = settings.login_url
    permission_denied_message = "Please login to add your products"
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


class DeleteProduct(CustomLoginRequiredMixin, View):

    login_url = settings.login_url
    permission_denied_message = "Please login to delete your products"

    """
    Delete Product View: Vender can delete their products from E-Deal.
    """

    def post(self, request):
        id = request.POST.get("pid")
        product = Product.objects.get(pk=id)
        product.delete()
        return JsonResponse(data={"message": "Data deleted successfully"}, status=200)
        

class CouponView(View):
    def get(self, request):
        context = {"coupons": Coupon.objects.all()}
        return render(request, "store/coupon.html", context)

    def post(self, request):
        id = request.POST.get("id")
        coupon = Coupon.objects.get(id=id)
        cart_amount = total(request)

        if coupon.coupon_type == "min":
            if cart_amount >= coupon.min:
                if coupon.discount_type == "in_rupees":
                    discount = coupon.discount
                else:
                    discount = (cart_amount * coupon.discount) / 100
            else:
                discount = 0

        elif coupon.coupon_type == "category":
            discounted_amount = pro_category(request, coupon.category)

            if coupon.discount_type == "in_rupees":
                if discounted_amount == 0:
                    discount = 0
                else:
                    discount = coupon.discount
            else:
                if coupon.upto:
                    if coupon.upto < (discounted_amount * coupon.discount) / 100:
                        discount = coupon.upto
                    else:
                        discount = (discounted_amount * coupon.discount) / 100
                else:
                    discount = (discounted_amount * coupon.discount) / 100

        elif coupon.coupon_type == "sub_cat":
            discounted_amount = pro_sub_category(request, coupon.sub_cat)

            if coupon.discount_type == "in_rupees":
                if discounted_amount == 0:
                    discount = 0
                else:
                    discount = coupon.discount

            else:
                if coupon.upto:
                    if coupon.upto < (discounted_amount * coupon.discount) / 100:
                        discount = coupon.upto
                    else:
                        discount = (discounted_amount * coupon.discount) / 100
                else:
                    discount = (discounted_amount * coupon.discount) / 100

        elif coupon.coupon_type == "brand":
            discounted_amount = pro_brand(request, coupon.brand)

            if coupon.discount_type == "in_rupees":
                if discounted_amount == 0:
                    discount = 0
                else:
                    discount = coupon.discount

            else:
                if coupon.upto:
                    if coupon.upto < (discounted_amount * coupon.discount) / 100:
                        discount = coupon.upto
                    else:
                        discount = (discounted_amount * coupon.discount) / 100
                else:
                    discount = (discounted_amount * coupon.discount) / 100

        elif coupon.coupon_type == "product":
            discounted_amount = prod(request, coupon.product)

            if coupon.discount_type == "in_rupees":
                if discounted_amount == 0:
                    discount = 0
                else:
                    discount = coupon.discount
            else:
                if coupon.upto:
                    if coupon.upto < (discounted_amount * coupon.discount) / 100:
                        discount = coupon.upto
                    else:
                        discount = (discounted_amount * coupon.discount) / 100
                else:
                    discount = (discounted_amount * coupon.discount) / 100

        return JsonResponse(
            data={"discount": discount, "message": "Applied successfully"},
            status=200,
        )


" Razorpay client object"
client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))


class PaymentView(CustomLoginRequiredMixin, View):
    login_url = settings.login_url
    permission_denied_message = "Access denied. Please login...!"
    """
    Payment View: When a Customer make a payment, their address will be saved. An order will be created and redirect to Rajorpay payment.
    """

    def post(self, request):
        mobile = request.POST.get("mobile")
        adrs = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip = request.POST.get("zip_code")
        discount = request.POST.get("discount")
        user = request.user

        address = Address.objects.create(
            user=user, mobile=mobile, address=adrs, city=city, state=state, zip_code=zip
        )

        cart = Cart(request)
        today = datetime.datetime.now(IST)
        sub_total = 0
        order = Order.objects.create(user=user, date=today, amount=sub_total)
        all_orderlines = []
        for product in cart.cart.values():
            quantity = int(product.get("quantity"))
            price = float(product.get("price"))
            product = int(product.get("product_id"))

            all_orderlines.append(
                OrderLine(user=user, order=order, product_id=product, quantity=quantity)
            )

            sub_total += price * quantity
        final_price = sub_total - float(discount)
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
            "sub_total": sub_total,
            "discount": discount,
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


class OrderView(CustomLoginRequiredMixin, View):

    """
    Order View: Shows all order of the authenticated Customer.
    """

    login_url = settings.login_url
    permission_denied_message = "Please login to view your orders"

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        result = {}
        for order in orders:
            orderlines = OrderLine.objects.filter(order=order)
            result[order] = orderlines

        context = {"result": result, "orders": orders}
        return render(request, "store/order.html", context)


class AddToWishlist(CustomLoginRequiredMixin, View):
    login_url = settings.login_url
    permission_denied_message = "Please login to add product to your wishlist"
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


class RemoveFromWishlist(CustomLoginRequiredMixin, View):
    login_url = settings.login_url
    permission_denied_message = "Please login to remove product from wishlist."
    """
    Remove Products: Remove products from the customer's wihslist.
    """

    def get(self, request):
        id = request.GET.get("pid")
        wishlist = Wishlist.objects.filter(Q(user=request.user) & Q(product_id=id))
        wishlist.delete()
        in_wishlist = Wishlist.objects.filter(user=request.user).count()
        return JsonResponse(
            data={"message": "Data deleted successfully", "in_wishlist": in_wishlist},
            status=200,
        )


class WishlistView(CustomLoginRequiredMixin, View):
    login_url = settings.login_url
    permission_denied_message = "Please login to view your wishlist"

    """
    Wishlist: Shows all products which are added to the customer's wishlist.
    """

    def get(self, request):
        wishlists = Wishlist.objects.filter(user=request.user)
        context = {"wishlists": wishlists}
        return render(request, "store/wishlist1.html", context)
