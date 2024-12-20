import sqlalchemy as sa
from database import metadata

transacoes = sa.Table(
  'Transacoes',
  metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('Tipo', sa.String(100), nullable=False),
  sa.Column('Conta', sa.String(7), nullable=False),
  sa.Column('Saldo_inicial', sa.Float()),
  sa.Column('Valor', sa.Float(), nullable=False),
  sa.Column('Saldo_disponivel', sa.Float()),
  sa.Column('Data', sa.Date),
  sa.Column('Hora', sa.Time)
)

usuarios = sa.Table(
  'Usuarios', 
   metadata,
   sa.Column('id', sa.Integer, primary_key=True),
   sa.Column('CPF', sa.String(11)),
   sa.Column('Nome', sa.String(50)),
   sa.Column('Senha', sa.String(15), nullable = False)
            )

contas = sa.Table(
  'Contas',
  metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('id_usuario', sa.Integer, sa.ForeignKey('Usuarios.id')),
  sa.Column('Conta', sa.String(7), nullable=False),
  sa.Column('Agencia', sa.String(4), nullable=False),
  sa.Column('Saldo', sa.Float)
)