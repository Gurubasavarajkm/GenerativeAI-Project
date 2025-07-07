from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    role: str

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str