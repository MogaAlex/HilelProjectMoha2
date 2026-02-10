from time import process_time

from flask import Flask
from jinja2.lexer import integer_re
from flask import render_template

app = Flask(__name__)



@app.route("/base")
def base():
    return render_template("base.html")


@app.route("/index")
def index():
    return render_template("index.html")

from __init__ import *

@app.route("/items")
def items():
    book1 = [product1, product2, product3]
    return render_template("items.html", products = book1)

app.run(debug=True)