
from passlib.context import CryptContext

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash(input: str):
    return hash_context.hash(input)

def verify(plain, hashed):
    return hash_context.verify(plain, hashed)
    
