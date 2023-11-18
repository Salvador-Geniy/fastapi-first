import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def convert_password_to_hash(password: str) -> str:
    """Base method with hashlib library"""
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    hashed_password = hash_object.hexdigest()

    return hashed_password


def get_password_hash(password: str) -> str:
    """Custom method with passlib library"""

    hashed_password = pwd_context.hash(password)

    return hashed_password


def verify_user_password(password: str, hashed_password: str) -> bool:
    """Function for check user password and password from database"""
    result = pwd_context.verify(secret=password, hash=hashed_password)
    return result
