import flask
import flask_restful as fr
from flask_restful import reqparse
from data import db_session
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument("name", required=True)
parser.add_argument("email", required=True)
parser.add_argument("password", required=True)


def abort_if_not_found(user_id):
    dbs = db_session.create_session()
    user = dbs.query(User).get(user_id)
    if not user:
        fr.abort(404, message=f"User {user_id} not found")


class UserResource(fr.Resource):
    def get(self, user_id):
        abort_if_not_found(user_id)
        dbs = db_session.create_session()
        user = dbs.query(User).get(user_id)
        return flask.jsonify({"user": user.to_dict(only=("name", "email", "balance"))})

    def delete(self, user_id):
        abort_if_not_found(user_id)
        args = parser.parse_args()
        if not len(args.keys()) or not all(key in ("name", "email", "password") for key in args.keys()):
            return flask.make_response(flask.jsonify({"error": "Bad Request"}), 400)
        dbs = db_session.create_session()
        user = dbs.query(User).get(user_id)
        if not user.check_password(args.get("password")) or user.email != args.get("email") or user.name != args.get(
                "name"):
            return flask.make_response(flask.jsonify({"error": "Wrong password or email"}))
        dbs.delete(user)
        dbs.commit()
        dbs.close()
        return flask.jsonify({"success": "OK"})


class UserListResource(fr.Resource):
    def get(self):
        dbs = db_session.create_session()
        users = dbs.query(User).all()
        return flask.jsonify({"users": [user.to_dict(only=("name", "email", "balance")) for user in users]})

    def post(self):
        args = parser.parse_args()
        if not len(args.keys()) or not all(key in ("name", "email", "password") for key in args.keys()):
            return flask.make_response(flask.jsonify({"error": "Bad Request"}), 400)
        dbs = db_session.create_session()
        user = dbs.query(User).filter(User.email.is_(args.get("email"))).first()
        if user:
            return flask.make_response(flask.jsonify({"error": "User with this email is already registered"}), 400)
        user = User(name=args.get("name"), email=args.get("email"))
        user.set_password(args.get("password"))
        dbs.add(user)
        dbs.commit()
        return flask.jsonify({"id": user.id})