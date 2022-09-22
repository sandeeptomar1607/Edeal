// Filter Product category wise
(function () {
    const buttons = document.querySelectorAll(".category-btn")
    const storeProducts = document.querySelectorAll(".store-product")
    buttons.forEach((button) => {
        button.addEventListener('click', (e) => {
            const filter = e.target.dataset.filter
            console.log(filter)

            storeProducts.forEach((item) => {
                if (filter == 'all') {
                    item.style.display = 'block'
                } else {
                    if (item.classList.contains(filter)) {
                        item.style.display = 'block'
                    } else {
                        item.style.display = 'none'
                    }
                }
            })
        })
    })

})();


const search = () => {
    const searchbox = document.getElementById("search").value.toUpperCase();
    const product = document.querySelectorAll(".s-product")
    const pname = document.getElementsByClassName("dropdown-item")

    for (var i = 0; i < pname.length; i++) {
        let match = pname[i];
        if (match) {
            let textvalue = match.textContent || match.innerHTML

            if (textvalue.toUpperCase().indexOf(searchbox) > -1) {
                product[i].style.display = "block";
            } else {
                product[i].style.display = "none";
            }
        }
    }

}


// Product scroller
$(document).on('click', '.left', function () {
    left = $(this).closest('.scroll-images');
    left.scrollLeft(-50)
    // if (left.scrollLeft() == 0) {
    //     $(this).fadeOut()
    // }
})
$(document).on('click', '.right', function () {
    right = $(this).closest('.scroll-images');
    right.scrollLeft(50)
    // if (right.scrollLeft() == 0) {
    //     $(this).fadeOut()

    // }
})



// SignUp 
$('#signup').click(function () {

    let fname = $('#id_first_name').val()
    let lname = $('#id_last_name').val()
    let email = $('#id_email').val()
    let mobile = $('#id_mobile').val()
    let role = $('#id_role').val()
    let password1 = $('#id_password1').val()
    let password2 = $('#id_password2').val()
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val()

    myData = { first_name: fname, last_name: lname, email: email, mobile: mobile, role: role, password1: password1, password2: password2, csrfmiddlewaretoken: csrftoken };

    $.ajax({
        url: "/signup/",
        method: "POST",
        data: myData,
        dataType: "json",
        success: function (data) {

            $("#exampleModal").hide();
            $("#loginid").click();
        },
        error: function (error) {
            alert('error; ' + eval(error));
        }
    })
})

// Add Product
$('#addproduct').click(function () {

    let myData = new FormData($("#myForm")[0]);

    $.ajax({
        url: "/addproduct/",
        method: "POST",
        contentType: false,
        processData: false,
        data: myData,
        success: function (data) {

            console.log("success")
            window.location = '/venderHome/';
        },
        error: function (error) {
            alert('error; ' + eval(error));
        }
    })
})


// Delete Product
$(document).on("click", '.i-del', function () {
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val()
    let id = $(this).attr("data-pid");

    myData = { pid: id, csrfmiddlewaretoken: csrftoken }
    myThis = this

    $.ajax({
        url: "/deleteproduct/",
        method: "POST",
        data: myData,
        success: function (data) {
            $(myThis).closest('.prodiv').fadeOut()
        },

        error: function (error) {
            console.log("failed")
        }
    })
})


// Add To Cart
$(document).on('click', '.add-to-cart', function () {
    let id = $(this).attr("data-pid");
    myThis = this
    myData = { pid: id }
    $.ajax({
        url: "/add/",
        method: "GET",
        data: myData,
        success: function (data) {
            $('#nav-cart').text("(" + data.product_in_cart + ")")
            $('#nav-cart').css('color', 'rgb(240, 92, 92)')
            $(myThis).text(" Added To Cart")
            $(myThis).closest('.pro-add').css('background-color', 'rgb(6, 143, 6)')
        },
        error: function (error) {
            console.log("failed")
        }

    })
})


// Buy Now
$(document).on('click', '.buy-now', function () {
    let id = $(this).attr("data-pid");
    myThis = this
    myData = { pid: id }
    $.ajax({
        url: "/add/",
        method: "GET",
        data: myData,
        success: function (data) {
            $('#nav-cart').text("(" + data.product_in_cart + ")")
            window.location = '/cart-detail/';
        },
        error: function (error) {
            console.log("failed")
        }
    })
})


// Increment product in the Cart.
$(document).on('click', '.increment', function () {
    let id = $(this).attr("data-pid");

    myData = { pid: id }
    myThis = this

    $.ajax({
        url: "/item_increment/",
        method: "GET",
        data: myData,
        success: function (data) {
            $(myThis).siblings('.quantity').text(data.quantity)

            item_total = $('.total').filter(`[data-pid=${id}]`);
            item_total.text('Total: ₹ ' + data.total)

            amount = $("#amount").text()
            let total = Number(amount) + data.price
            $("#amount").text(total)
        },

        error: function (error) {
            console.log("failed")
        }
    })
})


// Decrement product in the Cart.
$(document).on('click', '.decrement', function () {
    let id = $(this).attr("data-pid");

    myData = { pid: id }
    myThis = this

    $.ajax({
        url: "/item_decrement/",
        method: "GET",
        data: myData,
        success: function (data) {
            $(myThis).siblings('.quantity').text(data.quantity)

            item_total = $('.total').filter(`[data-pid=${id}]`);
            item_total.text('Total: ₹ ' + data.total)

            amount = $("#amount").text()
            let total = Number(amount) - data.price
            $("#amount").text(total)
        },

        error: function (error) {
            console.log("failed")
        }
    })
})


// Clear ITEM from cart
$(document).on('click', '.item-del', function () {
    let id = $(this).attr("data-pid");

    myData = { pid: id }
    myThis = this

    $.ajax({
        url: "/item_clear/",
        method: "GET",
        data: myData,
        success: function (data) {
            $('#nav-cart').text("(" + data.product_in_cart + ")")
            $('#nav-cart').css('color', 'rgb(240, 92, 92)')

            $(myThis).closest('.cart-div').fadeOut()
        },
        error: function (error) {
            console.log("failed")
        }
    })
})


// Address Form Validation
$("#proceed-to-pay").click(function () {

    mobile = $('#mobile-number').val()
    console.log($.type((mobile)))
    address = $('#address').val()
    city = $('#city').val()
    state = $('#state').val()
    zip = $('#zip-code').val()
    console.log(mobile)
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val()


    if (address == "") {
        $('#address-error').text(" *address can not be empty")
        $('#address-error').css({ "display": "block", "color": "red", "font-size": '70%' });
    } else {
        $('#address-error').css({ "display": "none" });
    }

    if (city == "") {
        $('#city-error').text(" *city can not be empty")
        $('#city-error').css({ "display": "block", "color": "red", "font-size": '70%' });
    } else {
        $('#city-error').css({ "display": "none" });
    }

    if (state == "") {
        $('#state-error').text(" *state Number can not be empty")
        $('#state-error').css({ "display": "block", "color": "red", "font-size": '70%' });
    } else {
        $('#state-error').css({ "display": "none" });
    }

    if (zip == "") {
        $('#zip-error').text(" *zip-code Number can not be empty")
        $('#zip-error').css({ "display": "block", "color": "red", "font-size": '70%' });
    } else {
        $('#zip-error').css({ "display": "none" });
    }


    if (mobile == "") {
        $('#mobile-error').text("*mobile Number can not be empty")
        $('#mobile-error').css({ "display": "block", "color": "red", "font-size": '70%' });

    } else if ((mobile.length != 10)) {
        $('#proceed-to-pay').removeAttr("type").attr("type", "button");
        $('#mobile-error').text("*Invalid Mobile Number")
        $('#mobile-error').css({ "display": "block", "color": "red", "font-size": '70%' });
        return false;

    } else {
        $('#proceed-to-pay').removeAttr("type").attr("type", "submit");
        $('#mobile-error').css({ "display": "none" });
    }

    if ((mobile == "") || (address == "") || (city == "") || (state == "") || (zip == "")) {
        $('#proceed-to-pay').removeAttr("type").attr("type", "button");
    } else {
        $('#proceed-to-pay').removeAttr("type").attr("type", "submit");

    }
})


// Add/Remove from Wishlist
$(document).on('click', '.wishlist', function () {
    console.log("clicked")
    let id = $(this).attr("data-pid");

    myData = { pid: id }
    myThis = this

    if ($(this).css("color") == "rgb(255, 0, 0)") {

        $.ajax({
            url: "/remove-from-wishlist/",
            method: "GET",
            data: myData,
            success: function (data) {
                $(myThis).css("color", "gray")
                $('#nav-wishlist').text(data.in_wishlist)
            },
            error: function (error) {
                console.log("failed")
            }
        })
    }
    else {
        $.ajax({
            url: "/wishlist/",
            method: "GET",
            data: myData,
            success: function (data) {
                $('#nav-wishlist').text(data.in_wishlist)

                $(myThis).css("color", "red")
            },

            error: function (error) {
                console.log("failed")
            }
        })
    }
})


// Add To Cart Button in wishlist
$(document).on('click', '.wishlist-cart', function () {
    let id = $(this).attr("data-pid");
    myThis = this
    myData = { pid: id }
    $.ajax({
        url: "/add/",
        method: "GET",
        data: myData,
        success: function (data) {
            $('#nav-cart').text(data.product_in_cart)
            $(myThis).closest('.wishlist-item').fadeOut()

            $.ajax({
                url: "/remove-from-wishlist/",
                method: "GET",
                data: myData,
                success: function (data) {
                    $(myThis).css("color", "black")
                    $('#nav-wishlist').text(data.in_wishlist)
                    $('.wish-alert').css({ "display": "block" });
                },

                error: function (error) {
                    console.log("failed")
                }
            })
        },
        error: function (error) {
            console.log("failed")
        }
    })
})


$('#login-btn').click(function () {
    email = $('#email-id').val()
    pass = $('#pass-id').val()
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val()

    if (email == "") {
        $('#email-error').text("*Email is required.")
        $('#email-error').css({ "display": "block", "color": "red", "font-size": '70%' });
    } else {
        $('#email-error').css({ "display": "none" });
    }

    if (pass == "") {
        $('#pass-error').text("*Enter password")
        $('#pass-error').css({ "display": "block", "color": "red", "font-size": '70%' });
    } else {
        $('#pass-error').css({ "display": "none" });
    }

    if ((email != "") && (pass != "")) {

        myData = { email: email, password: pass, csrfmiddlewaretoken: csrftoken }
        $.ajax({
            url: "/login/",
            method: "POST",
            data: myData,
            success: function (data) {
                if (data.role == 'vender') {
                    window.location = '/venderHome/';
                }
                else if (data.role == 'customer') {
                    window.location = '/';
                }
            },

            error: function (error) {
                $('#login-error').text("Email or Password is incorrect.")
                $('#login-error').css({ "display": "block" });

            }

        })
    }

})



// Update First name and Last Name
$('#p-edit').click(function () {
    update_btn = $(this).text()
    if (update_btn == "Edit") {
        $(this).text("Cancel")
        $('.pi').removeAttr("readonly")
        $('#save-pi').css({ "display": "block" })
    }
    else {
        $(this).text("Edit")
        $('.pi').attr("readonly", "true")
        $('#save-pi').css({ "display": "none" })

    }
})

$('#save-pi').click(function () {
    f_name = $('#f-name').val()
    l_name = $('#l-name').val()
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val()

    if (f_name == "") {
        $('#f-edit-error').text(" *Required")
        $('#f-edit-error').css({ "display": "block", "color": "red", "font-size": '70%' });
    } else if (l_name == "") {
        $('#l-edit-error').text(" *Required")
        $('#l-edit-error').css({ "display": "block", "color": "red", "font-size": '70%' });
    }
    else {
        myData = { first_name: f_name, last_name: l_name, csrfmiddlewaretoken: csrftoken }
        $.ajax({
            url: "/profile/",
            method: "POST",
            data: myData,
            success: function (data) {
                $("#p-edit").text("Edit")
                $('.pi').attr("readonly", "true")
                $('#save-pi').css({ "display": "none" })
                $('#r-user').text(data.f_name + " " + data.l_name)
                $('#f-edit-error').css({ "display": "none" });
                $('#l-edit-error').css({ "display": "none" });


            },

            error: function (error) {
                console.log('not')

            }

        })
    }
})


// Update Email address
$('#e-edit').click(function () {
    update_btn = $(this).text()
    if (update_btn == "Edit") {
        $(this).text("Cancel")
        $('#p-email').removeAttr("readonly")
        $('#save-email').css({ "display": "block" })
    }
    else {
        $(this).text("Edit")
        $('#p-email').attr("readonly", "true")
        $('#save-email').css({ "display": "none" })

    }
})


$('#save-email').click(function () {
    email = $('#p-email').val()
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val()

    if (email == "") {
        $('#e-edit-error').text(" *Email can't be empty")
        $('#e-edit-error').css({ "display": "block", "color": "red", "font-size": '70%' });
    }
    else {
        myData = { email: email, csrfmiddlewaretoken: csrftoken }
        $.ajax({
            url: "/profile/",
            method: "POST",
            data: myData,
            success: function (data) {
                $("#e-edit").text("Edit")
                $('#p-email').attr("readonly", "true")
                $('#save-email').css({ "display": "none" })
                $('#e-edit-error').css({ "display": "none" });
                console.log("updated")
            },

            error: function (error) {
                console.log('not')

            }

        })
    }
})



// Update Mobile Number
$('#m-edit').click(function () {
    update_btn = $(this).text()
    if (update_btn == "Edit") {
        $(this).text("Cancel")
        $('#p-mobile').removeAttr("readonly")
        $('#save-mobile').css({ "display": "block" })
    }
    else {
        $(this).text("Edit")
        $('#p-mobile').attr("readonly", "true")
        $('#save-mobile').css({ "display": "none" })

    }
})


$('#save-mobile').click(function () {
    mobile = $('#p-mobile').val()

    var csrftoken = $('input[name=csrfmiddlewaretoken]').val()
    if (mobile == "") {
        $('#m-edit-error').text(" *Mobile No. can't be empty")
        $('#m-edit-error').css({ "display": "block", "color": "red", "font-size": '70%' });
    } else if (mobile.length != 10) {
        $('#m-edit-error').text(" *Mobile No. must be 10 digit long")
        $('#m-edit-error').css({ "display": "block", "color": "red", "font-size": '70%' });
    }
    else {
        myData = { mobile: mobile, csrfmiddlewaretoken: csrftoken }
        $.ajax({
            url: "/profile/",
            method: "POST",
            data: myData,
            success: function (data) {
                $("#m-edit").text("Edit")
                $('#p-mobile').attr("readonly", "true")
                $('#save-mobile').css({ "display": "none" })
                $('#m-edit-error').css({ "display": "none" });

                console.log("updated")
            },

            error: function (error) {
                console.log('not')

            }

        })
    }
})


// Apply coupon
$(document).on('change', '.sel-coupon', function () {
    coupon_id = $('.sel-coupon').val()
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val()

    myData = { id: coupon_id, csrfmiddlewaretoken: csrftoken }

    $.ajax({
        url: "/coupon/",
        method: "POST",
        data: myData,
        success: function (data) {
            $('#cart-discount').val(data.discount);
            if (data.discount == 0) {
                $('#apply').css({ "display": "none" });

                $('#not-apply').css({ "display": "block", "color": "red", "font-size": '70%' });
            }
            else {
                $('#not-apply').css({ "display": "none" });

                $('#apply').css({ "display": "block" });
            }
            console.log(data.discount)
        },
        error: function (error) {
            console.log('not')
        }
    })
})