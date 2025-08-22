import bcrypt

def hash_password(password: str) -> bytes:
    """Хэширует пароль пользователя"""
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    """Проверяет соответствие введенного пароля и захэшированного"""
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


