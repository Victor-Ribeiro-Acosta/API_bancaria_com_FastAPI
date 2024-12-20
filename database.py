import databases
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

metadata = sa.MetaData()

conect_args = {"check_same_thread": False}
DATABAS_URL = "sqlite:///./banco.sqlite"

database = databases.Database(DATABAS_URL)

engine = sa.create_engine(DATABAS_URL)

sessao = sessionmaker(autocommit = False, autoflush = False, bind=engine)

# Criar sessão no banco de dados
def get_db():
  session = sessao()
  try:
      yield session
  finally:
    session.close()