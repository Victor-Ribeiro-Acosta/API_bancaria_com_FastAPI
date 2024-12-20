from fastapi import HTTPException, status
from random import choice
from database import database
from models.models import contas, usuarios

class CriarConta():
  def __init__(self):
    self.algarismos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    self.montagem_conta = []
    self.conta = ''
    self.AGENCIA = '0001'


  
  def criar_conta(self):
    for i in range(0, 7):
       self.montagem_conta.append(choice(self.algarismos))
  
    self.conta = ''.join(self.montagem_conta)
    return self.conta


  
  async def cadastrar_conta(self, cpf):

    numero_conta = self.criar_conta()

    query_usuario = usuarios.select().where(usuarios.c.CPF == cpf)
    usuario = await database.fetch_one(query_usuario)
    
    if not usuario:
      raise HTTException(status_code = status.NOT_FOUND, detail="Usuário não encontrado!")
    query_conta = contas.insert().values(
      id_usuario = usuario['id'],
      Conta = numero_conta,
      Agencia = self.AGENCIA,
      Saldo = 0.0
    )

    id_result = await database.execute(query_conta)
    return {"Conta": numero_conta, 'id': id_result}

