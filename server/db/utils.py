import bcrypt

def hash(unhashed_password: str):
    bytes = unhashed_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes, salt)
    return [hashed_password, salt]

def unhash(hashed_password: str, salt: str):
    pass