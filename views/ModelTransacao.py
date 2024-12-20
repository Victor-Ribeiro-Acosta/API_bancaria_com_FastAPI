from pydantic import BaseModel

class TransacaoOut(BaseModel):
  Tipo: str
  Conta: str
  Valor: float
  Saldo_disponivel: float