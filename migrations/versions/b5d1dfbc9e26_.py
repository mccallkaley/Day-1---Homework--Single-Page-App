"""empty message

Revision ID: b5d1dfbc9e26
Revises: 
Create Date: 2021-11-10 22:07:33.354450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5d1dfbc9e26'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=150), nullable=True),
    sa.Column('last_name', sa.String(length=150), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('password', sa.String(length=200), nullable=True),
    sa.Column('icon', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('pokemon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('base_hp', sa.Integer(), nullable=True),
    sa.Column('base_defense', sa.Integer(), nullable=True),
    sa.Column('base_attack', sa.Integer(), nullable=True),
    sa.Column('sprite_url', sa.String(length=500), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_updated', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pokemon_name'), 'pokemon', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_pokemon_name'), table_name='pokemon')
    op.drop_table('pokemon')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###