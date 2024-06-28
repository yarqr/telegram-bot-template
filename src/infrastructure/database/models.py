from dataclasses import asdict

from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.domain.user.entity import User


class BaseModel(DeclarativeBase):
    pass


class UserModel(BaseModel):
    __tablename__ = "users"
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    @classmethod
    def from_entity(cls, entity: User) -> "UserModel":
        return cls(**asdict(entity))

    def to_entity(self) -> User:
        return User(tg_id=self.tg_id)
