"""models updated

Revision ID: b5973a13255d
Revises: bd33f1636557
Create Date: 2024-03-07 09:42:39.945679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5973a13255d'
down_revision = 'bd33f1636557'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shopping_carts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('wishlists')
    op.drop_table('favourites')
    op.drop_table('shoppingCarts')
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=128), nullable=False))
        batch_op.drop_column('category')

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=128),
               nullable=False)

    with op.batch_alter_table('receipts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('details', sa.String(length=255), nullable=False))
        batch_op.drop_column('delivery_address')
        batch_op.drop_column('username')
        batch_op.drop_column('shipping_details')
        batch_op.drop_column('phone')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.String(length=20),
               type_=sa.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('receipts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('shipping_details', sa.VARCHAR(), nullable=False))
        batch_op.add_column(sa.Column('username', sa.VARCHAR(), nullable=False))
        batch_op.add_column(sa.Column('delivery_address', sa.VARCHAR(), nullable=False))
        batch_op.drop_column('details')

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(length=128),
               type_=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.VARCHAR(), nullable=False))
        batch_op.drop_column('name')

    op.create_table('shoppingCarts',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('product_id', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('favourites',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=False),
    sa.Column('price', sa.INTEGER(), nullable=False),
    sa.Column('onstock', sa.VARCHAR(), nullable=False),
    sa.Column('rating', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wishlists',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=False),
    sa.Column('price', sa.INTEGER(), nullable=False),
    sa.Column('onstock', sa.VARCHAR(), nullable=False),
    sa.Column('rating', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('shopping_carts')
    # ### end Alembic commands ###
