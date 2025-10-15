from __future__ import annotations

import base64
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status

from .config import get_settings


class AuthenticatedUser(Annotated[str, "authenticated-user"]):
    pass


async def require_jwt(request: Request) -> AuthenticatedUser:
    settings = get_settings()
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.jwt_public_key, algorithms=["RS256"], options={"verify_aud": False})
    except jwt.PyJWTError as exc:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    subject = payload.get("sub")
    if not subject:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid subject")

    return subject


def encode_basic_jwt(subject: str) -> str:
    settings = get_settings()
    if not settings.jwt_public_key:
        return base64.urlsafe_b64encode(subject.encode("utf-8")).decode("utf-8")
    raise NotImplementedError("JWT signing should be handled externally")


JWTDependency = Annotated[AuthenticatedUser, Depends(require_jwt)]
