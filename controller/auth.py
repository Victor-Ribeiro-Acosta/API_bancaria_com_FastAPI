from database import database, get_db
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.models import usuarios
from schemas.authModel import UserIn
from .security import validar_usuario
from services.conta import CriarConta
from services.exceptions import UnauthorizedError

from .security import criptografar_senha, validar_senha, criar_token_acesso

from views.AuthModel import UserOut, TokenOut

rota = APIRouter(prefix='/auth', tags=['Autorizações'])

@rota.post('/cadastrar_usuario', response_model = UserOut)
async def criar_usuario(usuario: UserIn):

  senha = criptografar_senha(usuario.Senha)
  
  query = usuarios.insert().values(
    Nome = usuario.Nome,
    CPF = usuario.CPF,
    Senha = senha
  )
  await database.execute(query)
  return usuario



@rota.post('/criar_token', response_model = TokenOut)
async def logar_usuario(data: OAuth2PasswordRequestForm = Depends(), session_db: Session = Depends(get_db)):
  
  usuario = session_db.query(usuarios).filter(usuarios.c.CPF == data.username).first()
  
  if not usuario or not validar_senha(data.password, usuario.Senha):
    raise UnauthorizedError(message = 'Usuario não cadastrado',status_code = status.HTTP_401_UNAUTHORIZED)
    
  token = criar_token_acesso(data={"nome": usuario.Nome})
  return {
    "token": token,
    "token_type": "bearer"}



@rota.post('/cadastrar_conta', dependencies=[Depends(validar_usuario)])
async def cadastrar(usuario: UserIn):
  conta = CriarConta()
  return await conta.cadastrar_conta(usuario.CPF)