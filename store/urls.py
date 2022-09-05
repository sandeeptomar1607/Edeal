from django.urls import path

from . import views
from .views import (
    AddProduct,
    AddToWishlist,
    DeleteProduct,
    Home,
    LoginView,
    OrderView,
    PaymentView,
    RemoveFromWishlist,
    SignUp,
    UpdateProduct,
    WishlistView,
    userLogout,
    venderHome,
)

app_name = "store"

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("venderHome/", venderHome.as_view(), name="venderHome"),
    path("signup/", SignUp.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", userLogout, name="logout"),
    path("addproduct/", AddProduct.as_view(), name="addproduct"),
    path("deleteproduct/", DeleteProduct.as_view(), name="deleteproduct"),
    path("updateproduct/", UpdateProduct.as_view(), name="updateproduct"),
    # Cart urls
    path("add/", views.cart_add, name="add"),
    path("item_clear/", views.item_clear, name="item_clear"),
    path("item_increment/", views.item_increment, name="item_increment"),
    path("item_decrement/", views.item_decrement, name="item_decrement"),
    path("cart_clear/", views.cart_clear, name="cart_clear"),
    path("cart-detail/", views.cart_detail, name="cart_detail"),
    path("payment/", PaymentView.as_view(), name="payment"),
    path("handlerequest/", views.handlerequest, name="handlerequest"),
    path("order/", OrderView.as_view(), name="order"),
    path("wishlist/", AddToWishlist.as_view(), name="wishlist"),
    path(
        "remove-from-wishlist/",
        RemoveFromWishlist.as_view(),
        name="remove-from-wishlist",
    ),
    path("wish/", WishlistView.as_view(), name="wish"),
]
