"""empty message

Revision ID: 04f4c1ed1326
Revises: 
Create Date: 2022-08-03 07:12:18.617331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04f4c1ed1326'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=64), nullable=True),
    sa.Column('prenom', sa.String(length=64), nullable=True),
    sa.Column('date_naissance', sa.Date(), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('adresse', sa.String(length=128), nullable=True),
    sa.Column('telephone', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('voitures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('marque', sa.String(length=32), nullable=True),
    sa.Column('immatriculation', sa.String(length=32), nullable=True),
    sa.Column('modele', sa.String(length=32), nullable=True),
    sa.Column('disponible', sa.Boolean(), nullable=True),
    sa.Column('couleur', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_voitures_immatriculation'), 'voitures', ['immatriculation'], unique=True)
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_location', sa.Date(), nullable=True),
    sa.Column('id_voiture', sa.Integer(), nullable=True),
    sa.Column('id_client', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_client'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['id_voiture'], ['voitures.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('locations')
    op.drop_index(op.f('ix_voitures_immatriculation'), table_name='voitures')
    op.drop_table('voitures')
    op.drop_table('clients')
    # ### end Alembic commands ###
