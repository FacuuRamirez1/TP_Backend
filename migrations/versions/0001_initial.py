"""Create catalog, clients and sales tables (without genre)."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("editorial", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("nombre", sa.String(150), nullable=False), sa.Column("pais", sa.String(100), nullable=False), sa.UniqueConstraint("nombre"))
    op.create_table("autor", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("nombre", sa.String(150), nullable=False), sa.Column("nacionalidad", sa.String(100), nullable=False))
    op.create_table("cliente", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("nombre", sa.String(150), nullable=False), sa.Column("email", sa.String(254), nullable=False), sa.UniqueConstraint("email"))
    op.create_index("ix_cliente_email", "cliente", ["email"])
    op.create_table("libro", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("isbn", sa.String(30), nullable=False), sa.Column("titulo", sa.String(250), nullable=False), sa.Column("precio", sa.Numeric(10, 2), nullable=False), sa.Column("stock", sa.Integer(), nullable=False), sa.Column("editorial_id", sa.Integer(), sa.ForeignKey("editorial.id"), nullable=False), sa.UniqueConstraint("isbn"), sa.CheckConstraint("precio > 0", name="ck_libro_precio_positivo"), sa.CheckConstraint("stock >= 0", name="ck_libro_stock_no_negativo"))
    op.create_index("ix_libro_editorial_id", "libro", ["editorial_id"])
    op.create_table("perfil_cliente", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("cliente_id", sa.Integer(), sa.ForeignKey("cliente.id"), nullable=False), sa.Column("telefono", sa.String(50), nullable=False), sa.Column("direccion", sa.String(250), nullable=False), sa.UniqueConstraint("cliente_id"))
    op.create_index("ix_perfil_cliente_cliente_id", "perfil_cliente", ["cliente_id"])
    op.create_table("libro_autor", sa.Column("libro_id", sa.Integer(), sa.ForeignKey("libro.id"), primary_key=True), sa.Column("autor_id", sa.Integer(), sa.ForeignKey("autor.id"), primary_key=True), sa.Column("rol", sa.String(20), nullable=False), sa.Column("orden", sa.Integer(), nullable=False), sa.CheckConstraint("orden >= 1", name="ck_libro_autor_orden_positivo"), sa.CheckConstraint("rol IN ('autor', 'coautor', 'traductor', 'ilustrador')", name="ck_libro_autor_rol"))
    op.create_index("ix_libro_autor_libro_id", "libro_autor", ["libro_id"])
    op.create_index("ix_libro_autor_autor_id", "libro_autor", ["autor_id"])
    op.create_table("venta", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("cliente_id", sa.Integer(), sa.ForeignKey("cliente.id"), nullable=False), sa.Column("fecha", sa.DateTime(timezone=True), nullable=False), sa.Column("total", sa.Numeric(12, 2), nullable=False), sa.CheckConstraint("total >= 0", name="ck_venta_total_no_negativo"))
    op.create_index("ix_venta_cliente_id", "venta", ["cliente_id"])
    op.create_table("renglon_venta", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("venta_id", sa.Integer(), sa.ForeignKey("venta.id"), nullable=False), sa.Column("libro_id", sa.Integer(), sa.ForeignKey("libro.id"), nullable=False), sa.Column("cantidad", sa.Integer(), nullable=False), sa.Column("precio_unitario", sa.Numeric(10, 2), nullable=False), sa.CheckConstraint("cantidad > 0", name="ck_renglon_cantidad_positivo"), sa.CheckConstraint("precio_unitario > 0", name="ck_renglon_precio_positivo"))
    op.create_index("ix_renglon_venta_id", "renglon_venta", ["venta_id"])
    op.create_index("ix_renglon_libro_id", "renglon_venta", ["libro_id"])


def downgrade() -> None:
    op.drop_table("renglon_venta")
    op.drop_table("venta")
    op.drop_table("libro_autor")
    op.drop_table("perfil_cliente")
    op.drop_table("libro")
    op.drop_table("cliente")
    op.drop_table("autor")
    op.drop_table("editorial")
