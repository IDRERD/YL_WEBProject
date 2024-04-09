import sqlalchemy as sa
import sqlalchemy.orm as orm
from db_session import SqlAlchemyBase
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy_serializer import SerializerMixin


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "products"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    # seller = sa.Column(sa.Integer)
    seller_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    seller = orm.relationship("User")
    tags = sa.Column(sa.String, nullable=True)
    price = sa.Column(sa.Integer, default=0)
    count = sa.Column(sa.Integer, default=0)
    in_stock = sa.Column(sa.Boolean, default=False)