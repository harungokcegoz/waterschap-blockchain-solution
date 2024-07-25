import os
from datetime import timedelta, datetime, timezone
from http.client import HTTPException

from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError  # Listed in the requirements as python-jose
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.services.agent_service import AgentService
from app.services.user_service import UserService

load_dotenv("app/db/.env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
        self.agent_service = AgentService(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, user_id: int):
        user = self.user_service.get_user_by_id(user_id)
        return user

    def authenticate_agent(self, email: str, password: str):
        agent = self.agent_service.get_agent_by_email(email)
        if not agent:
            return False
        if not self.verify_password(password, agent.hashed_password):
            return False
        return agent

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_active_user(self, token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
            user = self.user_service.get_user_by_id(user_id)
            if user is None:
                raise HTTPException(status_code=401, detail="User not found")
            return user
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def get_current_active_agent(self, token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            agent_id: int = payload.get("sub")
            if agent_id is None:
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
            agent = self.agent_service.get_agent_by_id(agent_id)
            if agent is None:
                raise HTTPException(status_code=401, detail="User not found")
            return agent
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")