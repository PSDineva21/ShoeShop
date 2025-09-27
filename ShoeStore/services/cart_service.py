carts = {}

def get_cart(user_email):
    return carts.get(user_email, [])

def add_to_cart(user_email, product, size, quantity=1):
    if user_email not in carts:
        carts[user_email] = []

    for item in carts[user_email]:
        if item["product"].id == product.id and item["size"] == size:
            item["quantity"] += quantity
            return

    carts[user_email].append({
        "product": product,
        "size": size,
        "quantity": quantity
    })

def remove_from_cart(user_email, product_id):
    if user_email in carts:
        carts[user_email] = [
            item for item in carts[user_email] if item["product"].id != product_id
        ]


def clear_cart(user_email):
    if user_email in carts:
        carts[user_email] = []