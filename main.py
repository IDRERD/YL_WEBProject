import flask

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "YliDrERdweBPrOjecTseCrEtKEyhOwThEheCkwIllyOuSeaRcHfORTHaT"


def main():
    app.run()


@app.route("/")
@app.route("/index")
def index():
    return flask.render_template("index.html", title="TradeMark'ed")

if __name__ == "__main__":
    main()