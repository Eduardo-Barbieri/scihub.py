import hashlib


def generate_md5_hash(content: bytes) -> str:
    return hashlib.md5(content).hexdigest()
