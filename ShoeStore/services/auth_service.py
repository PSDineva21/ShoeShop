users = []

def register_user(email, password, is_admin=False):
    for u in users:
        if u['email'] == email:
            return False, "Този имейл вече е регистриран!"

    new_user = {
        'email': email,
        'password': password,
        'is_admin': is_admin
    }
    users.append(new_user)

    print(f"Потвърждение за регистрация на {email}")
    return True, "Регистрацията е успешна!"

def login_user(email, password):
    for u in users:
        if u['email'] == email and u['password'] == password:
            return True, u
    # ако не намери нито един съвпадащ
    return False, "Грешен имейл или парола."
