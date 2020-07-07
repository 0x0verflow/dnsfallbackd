import hashlib
import uuid


def hash_key(key):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + key.encode()).hexdigest() + ":" + salt


def check_key(hashed_key, key, salt):
    return hashed_key is hashlib.sha256(salt.encode() + key.encode()).hexdigest()
