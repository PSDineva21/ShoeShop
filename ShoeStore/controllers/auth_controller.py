from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import auth_service

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form.get("role", "client")

        is_admin = True if role == "admin" else False

        success, msg = auth_service.register_user(email, password, is_admin)
        flash(msg)
        if success:
            return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        success, result = auth_service.login_user(email, password)
        if success:
            session["user"] = result
            flash("Успешен вход!")
            return redirect(url_for("index"))
        else:
            flash(result)

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Излязохте успешно.")
    return redirect(url_for("index"))