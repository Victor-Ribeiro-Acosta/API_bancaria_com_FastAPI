from services.exceptions import NotFoundError
from fastapi import status
from models.models import transacoes, contas
from database import database


class Transacao():
 
  async def executar_transacao(self, transacao):
    self.transacao = transacao.copy()
    
    query = contas.select().where(contas.c.Conta == self.transacao['Conta'])
    conta = await database.fetch_one(query)

    Saldo_inicial = conta['Saldo'] if conta else 0.0
    Valor = self.transacao['Valor']
    Saldo_disponivel = 0

    if self.transacao.Tipo.lower() == 'depósito':
      Saldo_disponivel = Saldo_inicial + Valor

    elif self.transacao.Tipo.lower() == 'saque':
      if Saldo_inicial < Valor:
        return {"Message":"Saldo insuficiente!"}
        
      Saldo_disponivel = Saldo_inicial - Valor

    query = transacoes.insert().values(
      Tipo = self.transacao.Tipo,
      Conta = self.transacao.Conta,
      Saldo_inicial = Saldo_inicial,
      Valor = Valor,
      Saldo_disponivel = Saldo_disponivel,
      Data = self.transacao.Data,
      Hora = self.transacao.Hora
    )

    id_result = await database.execute(query)
    return {
      'Tipo': self.transacao.Tipo,
      'Saldo inicial': Saldo_inicial,
      'Valor': Valor,
      'Saldo disponível': Saldo_disponivel,
      'id': id_result}

#if db != []:
#  transacao.saldo_inicial = db.pop()["saldo_disponível"]

#transacao.saldo_disponível = transacao.saldo_inicial + transacao.valor 
#db.append(transacao.model_dump())
#return transacao

  async def apresentar_extrato(self):
    query = transacoes.select()
    resultados = await database.fetch_all(query)
    return [dict(resultado) for resultado in resultados]

  
  async def atualizar_saldo(self):
    
    if not self.transacao.Conta:
      raise NotFoundError(message = 'Usuário sem conta cadastrada!', status_code = status.HTTP_404_NOT_FOUND)
      
    query = contas.update().where(contas.c.Conta == self.transacao.Conta).values(Saldo = self.transacao.Saldo_disponivel)
    
    retorno = await database.execute(query)
    if retorno == 0:
      raise NotFoundError(message = 'Não foi possível realizar a transação!', status_code = status.HTTP_404_NOT_FOUND)
      
    return {"message": "Operação realizada com sucesso"}