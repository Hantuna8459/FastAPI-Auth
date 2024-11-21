import uuid
import re
from datetime import datetime, timezone
from pydantic_core.core_schema import FieldValidationInfo
from pydantic import EmailStr, field_validator
from sqlmodel import (
    Field,
    SQLModel,
    Relationship,
    func,
)

class User(SQLModel, table=True):
    __tablename__ = "user"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    username: str = Field(unique=True, index=True, max_length=40)
    email: EmailStr|None = Field(
        default=None, unique=True, index=True, max_length=255
    )
    hashed_password:str = Field(nullable=False)
    first_name: str|None = Field(max_length=255,nullable=True, default=None, index=True)
    last_name: str|None = Field(max_length=255,nullable=True, default=None, index=True)
    address: str|None = Field(max_length=255,nullable=True, default=None, index=True)
    
    is_root: "UserRoot" = Relationship(back_populates="user",
                                       sa_relationship_kwargs={
                                           "uselist": False,
                                           "lazy": "selectin",
                                           "cascade":"all, delete-orphan",
                                        })
    
class UserRoot(SQLModel, table=True):
    __tablename__="user_root"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, unique=True
    )
    is_active: bool = Field(default=True, index=True)
    is_superuser: bool = Field(default=False, index=True)
    date_joined: datetime|None = Field(default_factory=lambda:datetime.now(timezone.utc))
    updated_at: datetime|None = Field(
        default=None,
        nullable=True,
        sa_column_kwargs={"onupdate":func.now()}
    )
    last_login: datetime|None = Field(
        default=None,
        nullable=True,
        sa_column_kwargs={"onupdate":func.now()}
    )
    
    user: "User" = Relationship(back_populates="is_root")
    
class UserPrivate(SQLModel):
    id: uuid.UUID
    password: str
    is_active: bool
    is_superuser: bool
    
class UserRegister(SQLModel):
    username: str = Field(unique=True, min_length=6, max_length=40)
    email: EmailStr|None = Field(default=None, unique=True, max_length=255)
    full_name: str|None = Field(default=None, max_length=255)
    address: str|None = Field(default=None, max_length=255)
    password: str = Field(max_length=255)
    password_confirm: str = Field(max_length=255)
    
    @field_validator("password")
    def password_validate(cls, value)->str:
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        if not re.search(r"[A-Z]",value):
            raise ValueError("Password must contain uppercase.")
        if not re.search(r"[a-z]",value):
            raise ValueError("Password must contain lowercase.")
        return value
    
    @field_validator("password_confirm")
    def passwords_match(cls, value, info: FieldValidationInfo):
        if 'password' in info.data and value != info.data["password"]:
            raise ValueError('passwords do not match')
        return value
    
class UserCreate(SQLModel):
    username: str = Field(unique=True, index=True, max_length=40)
    email: EmailStr|None = Field(
        default=None, unique=True, index=True, max_length=255
    )
    password:str = Field(index=True)
    full_name: str|None = Field(default=None, max_length=255, index=True)
    address: str|None = Field(default=None, max_length=255, index=True)
    is_root: object
       
class UserUpdateInfo(SQLModel):
    username: str = Field(unique=True, min_length=6, max_length=40)
    email: EmailStr|None = Field(default=None, unique=True, max_length=255)
    full_name: str|None = Field(default=None, max_length=255)
    address: str|None = Field(default=None, max_length=255)
    
class UserUpdatePassword(SQLModel):
    current_password: str = Field(min_length=6, max_length=255)
    new_password: str = Field(max_length=255)
    password_confirm: str = Field(max_length=255)
    
    @field_validator("new_password")
    def password_validate(cls, value):
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        if not re.search(r"[A-Z]",value):
            raise ValueError("Password must contain uppercase.")
        if not re.search(r"[a-z]",value):
            raise ValueError("Password must contain lowercase.")
        return value
    
    @field_validator("password_confirm")
    def passwords_match(cls, value, info: FieldValidationInfo):
        if 'new_password' in info.data and value != info.data["new_password"]:
            raise ValueError('passwords do not match')
        return value