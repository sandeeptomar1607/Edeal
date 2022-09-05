// Filter Product category wise
(function () {
    const buttons = document.querySelectorAll(".category-btn")
    const storeProducts = document.querySelectorAll(".store-product")
    buttons.forEach((button) => {
        button.addEventListener('click', (e) => {
            const filter = e.target.dataset.filter

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


// Update Product
$(document).on("click", ".i-edit", function () {

    let id = $(this).attr("data-pid");
    myData = { pid: id }
    $.ajax({
        url: "/updateproduct/",
        method: "GET",
        data: myData,
        success: function (data) {
            $('#pro-category').find(":selected").text(data.category);
            $('#pro-name').val(data.name)
            $('#pro-price').val(data.price)
            $('#pro-desc').val(data.description)
            image = $('#id_image').val(data.image)
            console.log(image)

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
            $('#nav-cart').text(data.product_in_cart)
            $(myThis).text("Added to cart")
            $(myThis).closest('.footer').css('background-color', 'rgb(12, 150, 12)')
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
            $('#nav-cart').text(data.product_in_cart)
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
    address = $('#address').val()
    city = $('#city').val()
    state = $('#state').val()
    zip = $('#zip-code').val()
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val()

    if (mobile == "") {
        $('#mobile-error').text(" *mobile Number can not be empty")
        $('#mobile-error').css({ "display": "block", "color": "red", "font-size": '70%' });
    } else {
        $('#mobile-error').css({ "display": "none" });
    }

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

    // myData = { mobile: mobile, address: address, city: city, mobile: mobile, state: state, zip_code: zip, csrfmiddlewaretoken: csrftoken };

    // $.ajax({
    //     url: "/payment/",
    //     method: "POST",
    //     data: myData,
    //     dataType: "json",
    //     success: function (data) {
    //         $('#cart-change').html("<p>test</p>")
    //         console.log("success", data)
    //     return false;
    //     },
    //     error: function (error) {
    //         alert('error; ' + eval(error));
    //     }
    // })

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
                $(myThis).css("color", "black")
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


