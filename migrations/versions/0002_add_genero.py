"""Add optional genre aggregation to books."""
from alembic import op
import sqlalchemy as sa

revision = "0002_add_genero"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("genero", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("nombre", sa.String(100), nullable=False), sa.UniqueConstraint("nombre"))
    op.add_column("libro", sa.Column("genero_id", sa.Integer(), sa.ForeignKey("genero.id"), nullable=True))
    op.create_index("ix_libro_genero_id", "libro", ["genero_id"])


def downgrade() -> None:
    op.drop_index("ix_libro_genero_id", table_name="libro")
    op.drop_column("libro", "genero_id")
    op.drop_table("genero")
