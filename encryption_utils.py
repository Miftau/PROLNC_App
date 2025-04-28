from cryptography.fernet import Fernet

# Generate once and save this key securely:
# key = Fernet.generate_key()
# print(key)
FERNET_KEY = b'JI7rHKlRHQdgwnOsJz5zYn2Ow8Pp5_J4UlQ7GeQ9JR8='
cipher = Fernet(FERNET_KEY)

def encrypt(msg: bytes) -> bytes:
    return cipher.encrypt(msg)

def decrypt(token: bytes) -> bytes:
    return cipher.decrypt(token)
