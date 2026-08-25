
import jwt
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone


class Security:
    def __init__(self, secret_key: str,
        algorithm: str = "HS256",):
        self.password_hash = PasswordHash.recommended()
        self.dummy_hash = self.password_hash.hash("dummypassword")
        self.secret_key = secret_key
        self.algorithm = algorithm

    def get_password_hash(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str,) -> bool:
        if hashed_password != "":
            return self.password_hash.verify(plain_password, hashed_password,)
        else:
            return self.password_hash.verify(plain_password, self.dummy_hash,)
    
    def create_access_token(self,data: dict, expires_delta: timedelta | None = None,) -> str:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})

        return jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def decode_access_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
        )