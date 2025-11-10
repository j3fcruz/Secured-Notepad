"""
encryption.py
----------------
Handles AES-256 encryption and decryption using a password-derived key.
Requires 'cryptography' library.
"""

import os
from base64 import urlsafe_b64encode
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("Warning: 'cryptography' library not found. Encryption disabled.")


def derive_key(password: str, salt: bytes) -> bytes:
    if not CRYPTO_AVAILABLE:
        raise RuntimeError("Cryptography library is not available.")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    return urlsafe_b64encode(kdf.derive(password.encode('utf-8')))


def encrypt_data(data: str, password: str) -> tuple[bytes, bytes]:
    """Encrypt plaintext and return token and salt."""
    if not CRYPTO_AVAILABLE:
        raise RuntimeError("Cryptography library is not available.")
    salt = os.urandom(16)
    key = derive_key(password, salt)
    token = Fernet(key).encrypt(data.encode('utf-8'))
    return token, salt


def decrypt_data(token: bytes, password: str, salt: bytes) -> str:
    """Decrypt encrypted token using password and salt."""
    if not CRYPTO_AVAILABLE:
        raise RuntimeError("Cryptography library is not available.")
    key = derive_key(password, salt)
    return Fernet(key).decrypt(token).decode('utf-8')
