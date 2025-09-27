from services import cart_service, catalog_service

orders = []

def create_order(user_email, address, payment_method):
    cart = cart_service.get_cart(user_email)
    if not cart:
        return False, "Кошницата е празна."

    for item in cart:
        if item["quantity"] > item["product"].stock:
            return False, f"Няма в наличност за продукт: {item['product'].name}"

    for item in cart:
        item["product"].stock -= item["quantity"]

    new_order = {
        "id": len(orders) + 1,
        "user_email": user_email,
        "items": cart.copy(),
        "address": address,
        "payment_method": payment_method
    }
    orders.append(new_order)

    cart_service.clear_cart(user_email)
    return True, f"Поръчка #{new_order['id']} е създадена успешно!"

