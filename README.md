
# Project Title

***`E-deal`*** is the name of the project. Basically it is a E-commerce website through which a user can buy product online. E-deal consists almost all category of products like Gocery, Electronics, Home & kitchen apliances, Beauty products etc. E-deal have a different world-wide partners(venders) like HP, Canon, Sony, MI, etc. It is the one stop solution for the online customers.

# Description 

E-deal Website is developed using Python (Django, a framework of python), CSS, Bootstrap, JacaScript JQuery and AJAX. It uses Postgres as a database. Talking about the project, it has all the essential features required for an e-commerce website. This project contains the user and admin side. Admin can manage products, venders, view logs and many more.

This project contains three type of users(role) which can access the E-deal based on their role permissoins.

### USER Roles

#### 1. Admin 

In this project, admin performs all the main functions like managing products, suppliers, users and much more. Admin has all the View permissions, Add permissions, Update permissions and Delete permissions.

#### 2. Vender 

Vender permorms all operations on products and coupons mainly.

- Vender can add new products and coupons to the E-deal.
- Vender can remove their products and coupons from E-deal.
- Vender can update their products and coupons on E-deal.
- Vender can view their products and coupons on E-deal.

#### 3. Customer 

From Customer account, he/she can view products and purchase it easily.

***Customer's available functionalities*** :

***`i. View all products`*** 

Customer Views all listed products on E-deal by all the venders. By clicking on a perticular product, they can view the all product related details.

***`ii. CRUD on Cart`*** 

- Customers has their cart. They can add multiple products to the cart and purchase them in a single order.
- They can remove products from their cart.
- They can increase or decrease the quantity of perticular product in the cart.

***`iii. CRUD on Wishlist`*** 

- Customers has their wishlist. If customer likes any product and want to save for later then, They can add that product to their wishlist to perchase it later.
- They can remove products from their wishlist.
- They can add products to the cart from wishlist.

***`iv. Coupons`***

- Customer can view coupons to the coupon section of their profile.
- Every coupon has their eligibility criteria and conditions.
- When Customer makes a payment, They can apply one coupon at a time. 
- If coupon will applied successfully then, discounted amount will be reduced from total amount of the order. 

***`v. Search product`***

- Search bar if located at the top of the webpage (on the navbar) They can Search products from the Search bar.
- When customer click on searched product, They can see the product details.

***`vi. Filter products`***

- Customer can filter products category wise, sub-category wise or brand wise.

***`vii. Orders`***

- Customer can place order by clicking `Pay Now` button.
- They can make online payment via `Net Banking`, `UPI` or `Card` by different banks.
- They can view their all Orders in the order section of profile with their status.

***`viii. Profile`***

- They can view their profile in which in the profile section.
- They update their profile.


#### Project setup
 
- Take a clone of the repo.
- Set the enviroment variables.
- Run command `docker compose build up`.

#### Rajorpay payment gateway
- Rajorpay is a payment gateway used in E-deal to take payments from the costomer on successfull order placement.







