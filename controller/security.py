from datetime import datetime, UTC, timedelta
from http import HTTPStatus
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.models import usuarios, contas
from database import get_db
from typing import Union


SECRET_KEY = "banco_api"
ALGORITM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 30


oauth2 = OAuth2PasswordBearer(tokenUrl = '/auth/criar_token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def criptografar_senha(senha: str):
  senha_crypt = pwd_context.hash(senha)
  return senha_crypt


def validar_senha(senha: str, senha_crypt: str):
  return pwd_context.verify(senha, senha_crypt)


def criar_token_acesso(data: dict, temp_expiracao: Union[timedelta, None] = None):
  encode_data = data.copy()

  if temp_expiracao:
    expire = datetime.now(UTC) + temp_expiracao
  else:
    expire = datetime.now(UTC) + timedelta(minutes=15)

  encode_data['exp'] = expire.timestamp()
  return jwt.encode(encode_data, SECRET_KEY, ALGORITM)


def validar_usuario(token:str = Depends(oauth2), session_db: Session = Depends(get_db)):
  excecao = HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail = "Não foi possível autorizar usuário!")

  try:
# decodificar token de acesso
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITM])
    
    nome: str = payload.get("nome")
    
    if not nome:
      raise excecao

  except JWTError:
    raise excecao

  try:
    usuario = session_db.query(usuarios).filter(usuarios.c.Nome == nome).first()

  except UnboundLocalError:
    raise excecao

  if usuario is None:
      raise excecao
    
  return usuario

  
  
