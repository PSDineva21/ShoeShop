from flask import Blueprint, render_template, request
from services import catalog_service

catalog_bp = Blueprint('catalog', __name__, url_prefix='/catalog')

@catalog_bp.route('/', methods=['GET'])
def catalog():
    query = request.args.get("q")
    color = request.args.get("color")
    max_price = request.args.get("max_price", type=float)
    size = request.args.get("size")
    in_stock = request.args.get("in_stock")

    products = catalog_service.search_products(
        query=query,
        color=color,
        max_price=max_price,
        size=size,
        in_stock=True if in_stock else None
    )
    return render_template("catalog.html", products=products)
