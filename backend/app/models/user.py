from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from app.models.refresh_token import RefreshToken

class UserBase(SQLModel):
    email:EmailStr = Field(unique=True, index=True, max_length=255)
    is_active:bool = True
    is_superuser:bool = True
    full_name:str|None = Field(default=None, max_length=255)

class User(UserBase, table=True):    
    user_id:int = Field(primary_key=True, index=True)
    hashed_password:str = Field(min_length=8, max_length=40)
    refresh_tokens:list["RefreshToken"] = Relationship(back_populates="owner", cascade_delete=True)