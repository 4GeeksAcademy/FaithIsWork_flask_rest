"""empty message

Revision ID: 0d662b2ebab8
Revises: 0004ee367505
Create Date: 2024-08-01 20:52:51.566950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d662b2ebab8'
down_revision = '0004ee367505'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.Column('people_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('favorite_planets')
    op.drop_table('favorite_people')
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=250),
               type_=sa.String(length=120),
               existing_nullable=False)

    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=250),
               type_=sa.String(length=120),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=250),
               existing_nullable=False)

    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=250),
               existing_nullable=False)

    op.create_table('favorite_people',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('people_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], name='favorite_people_people_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorite_people_user_id_fkey')
    )
    op.create_table('favorite_planets',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], name='favorite_planets_planet_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorite_planets_user_id_fkey')
    )
    op.drop_table('favorite')
    # ### end Alembic commands ###