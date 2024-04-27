import flask
import flask_restful as fr
from flask_restful import reqparse
from data import db_session
from data.products import Product
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument("name", required=True)
parser.add_argument("user_id", required=True)
parser.add_argument("price", required=True)
parser.add_argument("count", required=True)

user_parser = reqparse.RequestParser()
user_parser.add_argument("name", required=True)
user_parser.add_argument("email", required=True)
user_parser.add_argument("password", required=True)


def abort_if_not_found(product_id):
    dbs = db_session.create_session()
    product = dbs.query(Product).get(product_id)
    if not product:
        fr.abort(404, message=f"Product {product_id} not found")


class ProductListResource(fr.Resource):
    def get(self):
        dbs = db_session.create_session()
        products = dbs.query(Product).all()
        return flask.jsonify({"products": [product.to_dict(only=("name", "seller_id", "price", "count", "in_stock", "sell_date", "id")) for product in products]})

    def post(self):
        args = parser.parse_args()
        dbs = db_session.create_session()
        product = Product(name=args.get("name"), seller_id=args.get("seller_id"), price=args.get("price"), count=args.get("count"))
        product.in_stock = int(args.get("count")) > 0
        if int(args.get("count")) < 0:
            product.count = 0
        if int(args.get("price")) < 0:
            product.price = -int(args.get("price"))
        dbs.add(product)
        dbs.commit()
        return flask.jsonify({"id": product.id})


class ProductResource(fr.Resource):
    def get(self, product_id):
        abort_if_not_found(product_id)
        dbs = db_session.create_session()
        product = dbs.query(Product).get(product_id)
        return flask.jsonify({"product": product.to_dict(only=("name", "seller_id", "price", "count", "in_stock", "sell_date", "id"))})

    def delete(self, product_id):
        abort_if_not_found(product_id)
        args = user_parser.parse_args()
        dbs = db_session.create_session()
        user = dbs.query(User).filter(User.email.is_(args.get("email"))).first()
        if not user or user.name != args.get("name") or not user.check_password(args.get("password")):
            return flask.make_response(flask.jsonify({"error": "Wrong password or email"}), 400)
        product = dbs.query(Product).get(product_id)
        if product.seller_id != user.id:
            return flask.make_response(flask.jsonify({"error": "You are not the owner of this product"}), 400)
        dbs.delete(product)
        dbs.commit()
        return flask.jsonify({"success": "OK"})