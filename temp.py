from passlib.context import CryptContext

# -------------------- CREATE A PASSLIB CONTEXT ----------------#
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ----------------- CHECK WHETHER THE HASH PASSWORD AND USER ENTERED PASSWORD IS SAME OR NOT? -------------#
def pass_checker(user_pass, hash_pass):
    if pwd_context.verify(user_pass, hash_pass):
        return True
    else:
        return False


hash_password = pwd_context.hash(password)
