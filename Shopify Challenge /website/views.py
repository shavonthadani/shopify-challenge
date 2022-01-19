#views.py
#backend for home page, delete button and export to csv
#Developer: Shavon Thadani
#19/01/'22
from itertools import product
from flask import Blueprint,render_template, request, flash,jsonify, send_file
from flask_login import login_required, current_user
from .models import Product, User
from . import db
import json
import csv
views = Blueprint('views',__name__)

#home page
@views.route('/',methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        name = request.form.get('item_name')
        data = request.form.get('item_data')
        stock = request.form.get('item_stock')
        if len(name) == 0 or len(data) ==0:
            flash("Entry must have name and description", category= 'error')
        elif len(name) > 100 or len(data) >100:
            flash("Entries must be less than 100 characters", category= 'error')
        elif not stock.isdigit():
            flash("Stock must be a number.", category= 'error')
        else:
            new_item = Product(product_name=name, product_data=data, product_stock=stock, user_id=current_user.id)
            db.session.add(new_item)
            db.session.commit()
            flash("Item Added!", category= 'success')
    return render_template("home.html", user=current_user)

#delete item
@views.route('/delete-product',methods=['POST'])
def delete_product():
    product = json.loads(request.data)
    productId = product['itemId']
    product = Product.query.get(productId)
    if product:
        if product.user_id == current_user.id:
            db.session.delete(product)
            db.session.commit()
    return jsonify({})

#Create csv
@views.route('/to-csv',methods=['GET'])
def to_csv():
    with open('inventory.csv', 'w') as f:
        out = csv.writer(f)
        out.writerow(['id', 'product name','description','quantity','date'])
        data = User.query.get(current_user.id)
        for item in data.items:
            out.writerow([item.id, item.product_name, item.product_data, item.product_stock, item.date])
    return send_file('../inventory.csv')