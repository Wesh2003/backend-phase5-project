"""Initial migration.

Revision ID: 85878cb08d01
Revises: 
Create Date: 2024-03-17 16:31:58.491226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85878cb08d01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('category', sa.String(length=255), nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('onstock', sa.String(length=128), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('phone', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receipts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('delivery_address', sa.String(length=255), nullable=False),
    sa.Column('city', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shopping_carts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wishlists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_receipts',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('receipt_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['receipt_id'], ['receipts.id'], ),
    sa.PrimaryKeyConstraint('product_id', 'receipt_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_receipts')
    op.drop_table('wishlists')
    op.drop_table('shopping_carts')
    op.drop_table('reviews')
    op.drop_table('receipts')
    op.drop_table('users')
    op.drop_table('products')
    op.drop_table('admins')
    # ### end Alembic commands ###
