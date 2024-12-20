from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from controller import transacao, auth
from contextlib import asynccontextmanager
from database import database, metadata, engine
from services.exceptions import NotFoundError, UnauthorizedError


@asynccontextmanager
async def lifespan(app: FastAPI):
  await database.connect()
  from models import models
  metadata.create_all(engine)
  yield
  database.disconnect()

_metadata = [
  {"name": "Autorizações",
  "description": "Operações de cadastro e autenticação de usuarios do sistema"},
  {"name": "Transações",
   "description": "Operações de deposito, saque e extrato de transações"}
]

description ="""
# API Banco Digital

## Autorizações
Você pode:

- Cadastrar um novo usuário
- Logar com uma conta existente (um token será gerado para permitir acesso as funcionalidades da api).

## Transações

Você pode:
- Consultar o extrato das transações realizadas

Se estiver logado, você pode:
- Realizar depósitos de qualquer valor
- Saques de qualquer valor


"""

app = FastAPI(
  lifespan = lifespan,
  title = 'Documentação API Bancaria',
  version = "0.0.1",
  openapi_tags = _metadata,
  description=description
)

app.include_router(transacao.rota)
app.include_router(auth.rota)


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
  return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


@app.exception_handler(UnauthorizedError)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedError):
  return JSONResponse(status_code=exc.status_code, content={"message": exc.message})