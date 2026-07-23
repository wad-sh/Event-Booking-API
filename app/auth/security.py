from pwdlib import PasswordHash


pw_hash = PasswordHash.recommended()


def hash_pw (password: str) : 
    return pw_hash.hash(password)

def ver_pw ( password: str,hashed_pw:str) : 
    return pw_hash.verify(password,hashed_pw)