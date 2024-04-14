import flask
from flask_login import *
from data import db_session
from data.forms.register import RegisterForm
from data.products import Product
from data.users import User
from data.forms.login import LoginForm
from data.forms.products import ProductForm
from data.tag import Tag

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "YliDrERdweBPrOjecTseCrEtKEyhOwThEheCkwIllyOuSeaRcHfORTHaT"

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/market.db")
    app.run()


@app.route("/")
@app.route("/index")
def index():
    dbs = db_session.create_session()
    products = dbs.query(Product).all()
    return flask.render_template("index.html", title="TradeMark'ed", products=products  )


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return flask.render_template("register.html", title="Register", form=form, message="Passwords do not maych")
        dbs = db_session.create_session()
        if dbs.query(User).filter(User.email == form.email.data).first():
            return flask.render_template("register.html", title="Register", form=form, message="User with that email is already registered")
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        dbs.add(user)
        dbs.commit()
        return flask.redirect("/login")
    return flask.render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        dbs = db_session.create_session()
        user = dbs.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            current_user.id = user.id
            return flask.redirect("/")
        else:
            return flask.render_template("login.html", title="Authorization", message="Login or email invalid", form=form)
    return flask.render_template("login.html", title="Authorization", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    current_user.id = -1
    return flask.redirect("/")


@login_manager.user_loader
def load_user(user_id):
    dbs = db_session.create_session()
    return dbs.query(User).get(user_id)


@app.route("/products", methods=["POST", "GET"])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        dbs = db_session.create_session()
        seller = dbs.query(User).get(current_user.id)
        product = Product(name=form.name.data, seller_id=current_user.id, seller=seller, price=form.price.data, count=form.count.data, in_stock=True)
        for tg in form.tags.data:
            tag = dbs.query(Tag).filter(Tag.name == tg).first()
            if not tag:
                tag = Tag(name=tg)
                dbs.add(tag)
                dbs.commit()
            product.tags.append(tag)
        dbs.add(product)
        dbs.commit()
        return flask.redirect("/my_products")
    else:
        return flask.render_template("product.html", title="Add Product", paragraph_title="Add Product", form=form)

if __name__ == "__main__":
    main()