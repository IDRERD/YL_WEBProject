import glob

import flask
import sqlalchemy as sa
import datetime
from flask_login import *
from data import db_session
from data.forms.register import RegisterForm
from data.products import Product
from data.users import User
from data.forms.login import LoginForm
from data.forms.products import ProductForm
from data.tag import Tag
from data.forms.buy import BuyForm
from data.forms.tag import TagForm

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "YliDrERdweBPrOjecTseCrEtKEyhOwThEheCkwIllyOuSeaRcHfORTHaT"
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=7)

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/market.db")
    app.run()


@app.route("/")
@app.route("/index")
def index():
    dbs = db_session.create_session()
    products = dbs.query(Product).order_by(sa.desc(Product.id)).limit(10).all()
    img_names = [file[file.rfind('\\') + 1:file.rfind('.')] for file in glob.glob("static/images/products/*.png")]
    product_ids = [str(product.id) for product in products]
    img_names = [p_id if p_id in img_names else "default" for p_id in product_ids]
    return flask.render_template("index.html", title="TradeMark'ed", products=products, img_names=img_names)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return flask.render_template("register.html", title="Register", form=form, message="Passwords do not maych")
        dbs = db_session.create_session()
        if dbs.query(User).filter(User.email == form.email.data).first():
            return flask.render_template("register.html", title="Register", form=form,
                                         message="User with that email is already registered")
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
            return flask.render_template("login.html", title="Authorization", message="Login or email invalid",
                                         form=form)
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
    if isinstance(current_user, AnonymousUserMixin):
        return flask.redirect("/login")
    form = ProductForm()
    if form.validate_on_submit():
        dbs = db_session.create_session()
        seller = dbs.query(User).get(current_user.id)
        product = Product(name=form.name.data, seller_id=current_user.id, seller=seller, price=form.price.data,
                          count=form.count.data, in_stock=True)
        dbs.add(product)
        dbs.commit()
        return flask.redirect(f"/products/{product.id}")
    else:
        return flask.render_template("product.html", title="Add Product", paragraph_title="Add Product", form=form,
                                     tags=[], tag_form=TagForm(), product=None)


@app.route("/my_products")
def my_products():
    if not current_user.is_authenticated:
        return flask.redirect("/login")
    dbs = db_session.create_session()
    products = dbs.query(Product).order_by(sa.desc(Product.id)).filter(Product.seller_id == current_user.id)
    img_names = [file[file.rfind('\\') + 1:file.rfind('.')] for file in glob.glob("static/images/products/*.png")]
    product_ids = [str(product.id) for product in products]
    img_names = [p_id if p_id in img_names else "default" for p_id in product_ids]
    return flask.render_template("my_products.html", title="My Products", products=products, img_names=img_names)


@app.route("/products/<int:product_id>", methods=["POST", "GET"])
def edit_product(product_id):
    if isinstance(current_user, AnonymousUserMixin):
        return flask.redirect("/login")
    form = ProductForm()
    tag_form = TagForm()
    dbs = db_session.create_session()
    product = dbs.query(Product).get(product_id)
    dbs.close()
    form.name.data = product.name
    form.count.data = product.count
    form.price.data = product.price
    if flask.request.method == "POST":
        if flask.request.files.get("photo") is not None and flask.request.files["photo"].filename != "":
            flask.request.files["photo"].save(f"static/images/products/{product_id}.png")
    if flask.request.method == "GET":
        dbs = db_session.create_session()
        product = dbs.query(Product).get(product_id)
        if product and current_user.id == product.seller_id:
            form.name.data = product.name
            form.count.data = product.count
            form.price.data = product.price
        else:
            flask.abort(404)
    if tag_form.validate_on_submit():
        dbs = db_session.create_session()
        tag = dbs.query(Tag).filter(Tag.name == tag_form.tag_name.data).first()
        if not tag:
            tag = Tag(name=tag_form.tag_name.data)
            dbs.add(tag)
            dbs.commit()
        product = dbs.query(Product).get(product_id)
        product.tags.append(tag)
        dbs.commit()
        return flask.redirect(f"/products/{product_id}")
    if flask.request.form.get("action", 0) != 0:
        tag_name = flask.request.form["action"][3:]
        dbs = db_session.create_session()
        product = dbs.query(Product).get(product_id)
        tag = dbs.query(Tag).filter(Tag.name == tag_name).first()
        product.tags.remove(tag)
        dbs.commit()
        return flask.redirect(f"/products/{product_id}")
    if form.validate_on_submit():
        dbs = db_session.create_session()
        product = dbs.query(Product).get(product_id)
        if product and current_user.id == product.seller_id:
            product.name = form.name.data
            product.count = form.count.data
            product.price = form.price.data
            dbs.commit()
        else:
            flask.abort(404)
    dbs = db_session.create_session()
    product = dbs.query(Product).get(product_id)
    img_default = len(glob.glob(f"static/images/products/{product_id}.png")) == 0
    return flask.render_template("product.html", title="Edit product", form=form, paragraph_title="Edit product",
                                 tags=product.tags, tag_form=tag_form, product=product, img_default=img_default)


@app.route("/delete_product/<int:product_id>")
def delete(product_id):
    if isinstance(current_user, AnonymousUserMixin):
        return flask.redirect("/login")
    dbs = db_session.create_session()
    product = dbs.query(Product).get(product_id)
    if not isinstance(current_user, AnonymousUserMixin) and current_user.id == product.seller_id:
        dbs.delete(product)
        dbs.commit()
    return flask.redirect("/my_products")


@app.route("/buy_product/<int:product_id>", methods=["POST", "GET"])
def buy_product(product_id):
    if isinstance(current_user, AnonymousUserMixin):
        return flask.redirect("/login")
    form = BuyForm()
    dbs = db_session.create_session()
    product = dbs.query(Product).get(product_id)
    if form.validate_on_submit():
        quantity = form.count.data
        cost = product.price * quantity
        user = dbs.query(User).get(current_user.id)
        if user.balance < cost:
            return flask.render_template("buy_product.html", form=form, product=product,
                                         message="You have not enough money on your balance",
                                         title=f"Buy {product.name}")
        else:
            user.balance -= cost
            product.count -= quantity
            product.seller.balance += cost
            if product.count == 0:
                product.in_stock = False
            dbs.commit()
            return flask.redirect(f"/buy_product/{product_id}")
    img_default = len(glob.glob(f"static/images/products/{product_id}.png")) == 0
    return flask.render_template("buy_product.html", form=form, product=product, title=f"Buy {product.name}",
                                 img_default=img_default)


@app.route("/all_products", methods=["POST", "GET"])
def all_products():
    global search_tags
    show_mode = []
    order = "latest"
    desc = None
    if flask.session.get("price_from") is None:
        flask.session["price_from"] = ""
    if flask.session.get("price_to") is None:
        flask.session["price_to"] = ""
    if len(flask.session.get("search_tags", [])) == 0:
        flask.session["search_tags"] = []
    if flask.request.method == "POST":
        order = flask.request.form.get("order", "latest")
        show_mode = flask.request.form.getlist("show_mode")
        desc = flask.request.form.get("descending")
        new_tag_name = flask.request.form.get("tag_name", "")
        if new_tag_name:
            st = flask.session["search_tags"]
            st.append(new_tag_name)
            flask.session["search_tags"] = st
        if flask.request.form.get("del_tag") is not None:
            st = flask.session["search_tags"]
            st.remove(flask.request.form.get("del_tag")[3:])
            flask.session["search_tags"] = st
        flask.session["price_from"] = flask.request.form.get("price_from")
        flask.session["price_to"] = flask.request.form.get("price_to")
    tmporder = order[:]
    if order == "price":
        order = Product.price
    elif order == "stock":
        order = Product.count
    else:
        order = Product.id
    if desc is None:
        order = sa.desc(order)
    tags = [Tag(name=i) for i in flask.session.get("search_tags", [])]
    dbs = db_session.create_session()
    products = dbs.query(Product).filter(
        Product.in_stock.in_([True, False] if "out_of_stock" in show_mode else [True])).filter(Product.seller_id.is_not(
        -1 if isinstance(current_user, AnonymousUserMixin) or "your" in show_mode else current_user.id)).order_by(
        order).limit(100).all()
    if len(tags):
        products = list(filter(lambda x: any([i in tags for i in x.tags]), products))
    if flask.session.get("price_from"):
        products = list(filter(lambda x: x.price >= int(flask.session.get("price_from")), products))
    if flask.session.get("price_to"):
        products = list(filter(lambda x: x.price <= int(flask.session.get("price_to")), products))
    img_names = [file[file.rfind('\\') + 1:file.rfind('.')] for file in glob.glob("static/images/products/*.png")]
    product_ids = [str(product.id) for product in products]
    img_names = [p_id if p_id in img_names else "default" for p_id in product_ids]
    return flask.render_template("all_products.html", products=products, show_mode=show_mode, title="All products",
                                 order=tmporder, desc=desc, tags=tags, session=flask.session, img_names=img_names)


if __name__ == "__main__":
    main()
