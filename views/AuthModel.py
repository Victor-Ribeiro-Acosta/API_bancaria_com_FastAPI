
from pydantic import BaseModel

class UserOut(BaseModel):
  Nome: str
  CPF: str

class TokenOut(BaseModel):
  token: str
  token_type: str
