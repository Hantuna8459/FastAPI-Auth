from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

class UserBase(SQLModel):
    email:EmailStr = Field(unique=True, index=True, max_length=255)
    is_active:bool = True
    is_superuser:bool = False
    full_name:str|None = Field(default=None, max_length=255)

class User(UserBase, table=True):    
    user_id:int = Field(primary_key=True, index=True)
    hashed_password:str = Field(min_length=8, max_length=40)
    refresh_tokens:list["RefreshToken"] = Relationship(back_populates="owner", cascade_delete=True)
    
import uuid

class RefreshToken(SQLModel, table=True):
    __tablename__="refresh_tokens"
    
    token_id:uuid.UUID = Field(default_factory=uuid.uuid4 ,primary_key=True, index=True)
    token:str
    user_id:int = Field(foreign_key="user.user_id", nullable=False, ondelete="CASCADE")
    owner: User | None = Relationship(back_populates="refresh_tokens")

class Token(SQLModel):
    access_token: str
    token_type: str = 'bearer'

class TokenPayload(SQLModel):
    sub:str|None=None