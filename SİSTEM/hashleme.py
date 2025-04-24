import hashlib
import secrets

def hash_(data):
    data = data.encode("utf-8")
    hash_object = hashlib.sha256(data) 
    hashed_data = hash_object.hexdigest()
    return hashed_data
