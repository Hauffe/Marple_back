from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, make_response, current_app as app
)

from datetime import datetime as dt
from .models import db, User, Restriction, Ingredient, RestrictionEncoder
from flaskr.auth import login_required
from datetime import datetime
import pyrebase
import uuid
import json

config = {
    "apiKey": "AIzaSyAZbMMbdFR3zK8-giYMh1Dg5Q_pmgLrRMQ",
    "authDomain": "marple-3161a.firebaseapp.com",
    "databaseURL": "https://marple-3161a.firebaseio.com",
    "projectId": "marple-3161a",
    "storageBucket": "marple-3161a.appspot.com",
    "messagingSenderId": "348358607845",
    "appId": "1:348358607845:web:24063f823153fc00d5a50c",
    "measurementId": "G-4ZV65FBK7H"
}

firebase = pyrebase.initialize_app(config)
dbf = firebase.database();


bp = Blueprint('routes', __name__, url_prefix='/restrictions')


def load_restrictions():
    restrictions = dbf.child("Restriction").get()
    restriction_list = []
    for restriction_fb in restrictions.each():
        restriction_list.append(restriction_fb.val())

    return restriction_list


@bp.route('/')
@login_required
def index():
    restriction_list = load_restrictions()

    return render_template('restrictions/index.html', restrictions=restriction_list)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    restrictions = dbf.child("Restriction").get()
    restriction_list = []
    for restriction_fb in restrictions.each():
        restriction_list.append(restriction_fb.val())

    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        error = None

        if not name or not ingredients:
            error = 'Name is required.'

        ingredients_list = []
        count = 0
        for ingredient_name in ingredients.split(", "):
            ingredients_list.append(Ingredient("", count, ingredient_name))
            count += 1

        if error is None:
            new_restriction = Restriction(enable=True,
                                  id=restriction_list.__len__(),
                                  ingredients=ingredients_list,
                                  name=name)

            json_obj = json.dumps(new_restriction, cls=RestrictionEncoder)
            print(json.loads(json_obj))
            dbf.child("Restriction").child(name).set(json.loads(json_obj))

            return redirect(url_for('routes.index'))

        flash(error)

    return render_template('restrictions/create.html')


def get_product(id):
    product = Product.query.filter(Product.id == id).first()

    if product is None:
        abort(404, "Product id {0} doesn't exist.".format(id))

    return product


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    return redirect(url_for('routes.index'))


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    return render_template('restrictions/update.html', product=product)
