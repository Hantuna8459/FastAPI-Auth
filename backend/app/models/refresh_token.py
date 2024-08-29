from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)
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