from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import catalog_service

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def is_admin():
    user = session.get("user")
    return user and user.get("is_admin")

@admin_bp.before_request
def check_admin():
    if not is_admin():
        flash("Нямате достъп.")
        return redirect(url_for("index"))

@admin_bp.route("/")
def dashboard():
    products = catalog_service.get_all_products()
    return render_template("admin/dashboard.html", products=products)

@admin_bp.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        color = request.form["color"]
        sizes = request.form["sizes"].split(",")
        price = float(request.form["price"])
        stock = int(request.form["stock"])

        catalog_service.add_product(name, description, color, sizes, price, stock)
        flash("Продуктът е добавен успешно.")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/add_product.html")

@admin_bp.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = catalog_service.get_product_by_id(product_id)
    if not product:
        flash("Продуктът не е намерен.")
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        product.name = request.form["name"]
        product.description = request.form["description"]
        product.color = request.form["color"]
        product.sizes = request.form["sizes"].split(",")
        product.price = float(request.form["price"])
        product.stock = int(request.form["stock"])

        flash("Продуктът е редактиран успешно.")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/edit_product.html", product=product)


@admin_bp.route("/delete/<int:product_id>")
def delete_product(product_id):
    product = catalog_service.get_product_by_id(product_id)
    if product:
        catalog_service.products.remove(product)
        flash("Продуктът е изтрит.")
    return redirect(url_for("admin.dashboard"))