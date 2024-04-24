import sqlalchemy as sa
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from dataclasses import dataclass

product_tags = sa.Table("association", SqlAlchemyBase.metadata, sa.Column("products", sa.Integer, sa.ForeignKey("products.id")), sa.Column("tags", sa.Integer, sa.ForeignKey("tags.id")))


# @dataclass
class Tag(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "tags"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)

    def __eq__(self, other):
        return self.name == other.name