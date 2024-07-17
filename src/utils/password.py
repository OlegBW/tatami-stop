from argon2 import PasswordHasher

ph = PasswordHasher()


def get_password_hash(password):
    return ph.hash(password)


def verify_password(hashed_password, plain_password):
    try:
        return ph.verify(hashed_password, plain_password)
    except Exception:
        return False
