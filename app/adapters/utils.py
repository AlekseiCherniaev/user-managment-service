import re
import uuid
from datetime import timedelta, datetime

import jwt
import bcrypt
from app.config.config import settings
from app.domain.entities.user import User


def encode_jwt(
        payload: dict,
        private_key: str = settings.private_key_path.read_text(),
        algorithm: str = settings.ALGORITHM,
        expire_minutes: int = settings.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
        jti=str(uuid.uuid4()),
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.public_key_path.read_text(),
        algorithm: str = settings.ALGORITHM,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(
        token_type: str,
        token_data: dict,
        expire_minutes: int = settings.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: User) -> str:
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.access_token_expire_minutes,
    )


def create_refresh_token(user: User) -> str:
    jwt_payload = {
        "sub": user.username
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.refresh_token_expire_days),
    )


def hash_password(
        password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password=hashed_password)


def password_check_complexity(password: str) -> bool:
    # reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    password_regex = (
        r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    )
    pattern = re.compile(password_regex)
    return bool(pattern.match(password))


def user_to_dict(user):
    return {
        "id": str(user.id),
        "name": user.name,
        "surname": user.surname,
        "username": user.username,
        "phone_number": user.phone_number,
        "email": user.email,
        "role_id": user.role_id,
        "group_id": user.group_id,
        "image_path": user.image_path,
        "is_blocked": user.is_blocked,
        "active": user.active,
        "created_at": user.created_at,
        "modified_at": user.modified_at
    }
