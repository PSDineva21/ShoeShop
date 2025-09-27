from types import SimpleNamespace

products = []

def add_product(name, description, color, sizes, price, stock):
    new_product = SimpleNamespace(
        id=len(products) + 1,
        name=name,
        description=description,
        color=color,
        sizes=sizes,
        price=price,
        stock=stock
    )
    products.append(new_product)
    return new_product

def get_all_products():
    return products

def get_product_by_id(product_id):
    for p in products:
        if p.id == product_id:
            return p
    return None

def search_products(query=None, color=None, max_price=None, size=None, in_stock=None):
    results = products

    if query:
        results = [p for p in results if query.lower() in p.name.lower()]

    if color:
        results = [p for p in results if p.color.lower() == color.lower()]

    if max_price:
        results = [p for p in results if p.price <= max_price]

    if size:
        results = [p for p in results if size in p.sizes]

    if in_stock:
        results = [p for p in results if p.stock > 0]

    return results
