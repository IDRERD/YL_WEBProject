import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
import datetime


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "products"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    seller_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    seller = orm.relationship("User")
    tags = orm.relationship("Tag", secondary="association", backref="products")
    price = sa.Column(sa.Integer, default=0)
    count = sa.Column(sa.Integer, default=0)
    in_stock = sa.Column(sa.Boolean, default=False)
    sell_date = sa.Column(sa.DateTime, default=datetime.datetime.now())