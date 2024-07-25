from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    address: str
    phone_number: str
    email: str
    reward_requested: bool
    wallet_address: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserWalletUpdate(BaseModel):
    wallet_address: str


class UserToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


class EmailRequest(BaseModel):
    email: str


class BlockchainDTO(BaseModel):
    balance: dict 


class UserWithBalance(UserBase):
    blockchain_info: BlockchainDTO


class User(UserBase):
    user_id: int

    class Config:
        from_attribute = True
