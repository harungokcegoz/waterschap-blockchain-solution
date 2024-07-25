from sqlalchemy.orm import Session
from typing import List, Type
from app.models.models import UserModel
from app.schemas.user_schema import User, UserCreate, UserUpdate, UserWalletUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self) -> List[Type[UserModel]]:
        return self.db.query(UserModel).all()

    def get_user_by_id(self, user_id: int):
        return self.db.query(UserModel).filter(user_id == UserModel.user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(UserModel).filter(email == UserModel.email).first()

    def create_user(self, user_data: UserCreate):
        db_user = UserModel(**user_data.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user_data: UserUpdate):
        db_user = self.get_user_by_id(user_id)
        if db_user:
            for key, value in user_data.dict().items():
                setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def update_user_wallet(self, user_id: int, userWallet: UserWalletUpdate):
        db_user = self.get_user_by_id(user_id)
        if db_user:
            db_user.wallet_address = userWallet.wallet_address
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.get_user_by_id(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
        return db_user
