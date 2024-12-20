
from pydantic import BaseModel

class UserIn(BaseModel):
  Nome: str
  CPF: str
  Senha: str