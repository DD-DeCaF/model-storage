"""merge migrations organism_id and preferred_map

Revision ID: 19c7012eceb0
Revises: 83b6ba1af540, f55ed1a98c68
Create Date: 2018-11-27 09:38:33.895296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19c7012eceb0'
down_revision = ('83b6ba1af540', 'f55ed1a98c68')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
