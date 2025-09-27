from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import cart_service, catalog_service, order_service

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")

def is_logged_client():
    user = session.get("user")
    return user and not user.get("is_admin")

@cart_bp.before_request
def check_client():
    if not is_logged_client():
        flash("Само клиенти имат достъп до кошницата.")
        return redirect(url_for("index"))

@cart_bp.route("/")
def view_cart():
    user = session["user"]
    cart = cart_service.get_cart(user["email"])
    return render_template("cart.html", cart=cart)

@cart_bp.route("/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    if "user" not in session:
        flash("Моля, влезте в акаунта си.")
        return redirect(url_for("auth.login"))

    user = session["user"]
    size = request.form.get("size")
    quantity = int(request.form.get("quantity", 1))

    product = catalog_service.get_product_by_id(product_id)
    if not product:
        flash("Продуктът не е намерен.")
        return redirect(url_for("catalog.catalog"))

    cart_service.add_to_cart(user["email"], product, size, quantity)
    flash("Продуктът е добавен в количката!")
    return redirect(url_for("catalog.catalog"))


@cart_bp.route("/remove/<int:product_id>")
def remove_from_cart(product_id):
    user = session["user"]
    cart_service.remove_from_cart(user["email"], product_id)
    flash("Продуктът е премахнат от кошницата.")
    return redirect(url_for("cart.view_cart"))

@cart_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    user = session["user"]
    if request.method == "POST":
        address = request.form["address"]
        payment = request.form["payment"]

        success, msg = order_service.create_order(user["email"], address, payment)
        flash(msg)
        return redirect(url_for("catalog.catalog"))

    cart = cart_service.get_cart(user["email"])
    return render_template("checkout.html", cart=cart)