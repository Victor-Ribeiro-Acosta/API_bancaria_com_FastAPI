
from fastapi import APIRouter, status
from fastapi.params import Depends
from schemas.ModelTtransacao import TransacaoIn
from services.transacao import Transacao
from services.exceptions import NotFoundError
from views.ModelTransacao import TransacaoOut

from .security import validar_usuario

rota = APIRouter(prefix='/transaction', tags=['Transações'])

@rota.post('/transacao', response_model=TransacaoOut, dependencies=[Depends(validar_usuario)])
async def depositar(transacao: TransacaoIn):

  operacao = Transacao()
  resposta = await operacao.executar_transacao(transacao)
 
  if not resposta:
    return NotFoundError(message = 'Não foi possível realizar a operação!', status_code = status.HTTP_404_NOT_FOUND)
    
  await operacao.atualizar_saldo()
  return resposta
  


@rota.get('/extrato', response_model=list[TransacaoOut])
async def listar_transacoes():
  operacao = Transacao()
  return await operacao.apresentar_extrato()

