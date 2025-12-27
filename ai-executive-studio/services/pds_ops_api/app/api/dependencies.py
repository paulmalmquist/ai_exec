from __future__ import annotations

import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.db.database import SessionLocal

security = HTTPBasic()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def auth_guard(credentials: HTTPBasicCredentials = Depends(security)) -> dict:
    username = os.getenv("AUTH_USER", "admin")
    password = os.getenv("AUTH_PASS", "admin")
    if credentials.username != username or credentials.password != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    role_map = {
        username: os.getenv("AUTH_ROLE", "admin")
    }
    return {"user": credentials.username, "role": role_map.get(credentials.username, "analyst")}
