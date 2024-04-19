import sqlalchemy as sa
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False, unique=True)
    hashed_password = sa.Column(sa.String, nullable=True)
    products = orm.relationship("Product", back_populates="seller")
    balance = sa.Column(sa.Integer, nullable=False, default=0)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)