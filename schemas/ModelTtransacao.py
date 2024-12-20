from datetime import datetime

from pydantic import BaseModel

class TransacaoIn(BaseModel):
  Tipo: str
  Conta: str
  Valor: float
  Saldo_inicial: float = 0
  Saldo_disponivel: float = 0
  Data: datetime = datetime.now().date()
  Hora: datetime = datetime.now().time()