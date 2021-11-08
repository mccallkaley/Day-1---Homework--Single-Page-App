from flask import render_template, request, flash, g,redirect
from flask.helpers import url_for
from flask_wtf import *
import requests
from flask_login import login_required
from app.blueprints.auth.forms import  ProductForm 
from PIL import Image
from app.models import User, Product, Cart
import secrets
import os


from app.models import *
from .import bp as main

@main.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(main.root_path, 'static/product_pics', picture_fn)
    
    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

# # Create a item
# {
#     "name": new name
#     "description": new desc
#     "price": new price
#     "img": new img
#     "category_id":new cat id
# }
# route for  new product created
@main.route('/createproduct', methods=['GET','POST'])
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        print("Yes")
        print("Product shown", form.picture.data)

        product_data = {
        'name' : form.name.data,
        'description' : form.description.data,
        'user_id' : current_user.id,
        'img' : form.img,
        'price' : form.price.data
        }

        Product().from_dict(product_data)
        print("Product has been saved!")
        return redirect(url_for("index"))
    
    return render_template("create_product.html.j2", form=form)

@main.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html.j2', product=product)

@main.route('/addtocart/<int:product_id>', methods=['GET'])
@login_required
def addtocart(product_id):
    product_data = {
        'user_id' : current_user.id,
        'product_id' : product_id
    }
    check_product_in_cart = bool(Cart.query.filter_by(user_id = product_data['user_id'], product_id = product_data['product_id']).first())
    
    if check_product_in_cart == True:
        flash(f'Product already in your cart', 'danger')
        return redirect(url_for('cart'))
    else:
        Cart().from_dict(product_data)
        flash(f'Product has been added to your cart', 'success')
        return redirect(url_for('cart'))


@main.route('/cart', methods=['GET'])
@login_required
def cart():
    user_cart = Cart.query.filter_by(user_id = current_user.id).all()
    cart_products = (Product.query.filter_by(id = product.product_id).first() for product in user_cart)
    products = list(cart_products)
    total = Product().total_price(user_id= current_user.id)
    return render_template("cart.html.j2", products = products, total = total)


@main.route('/deletefromcart/<int:product_id>', methods=['GET'])
@login_required
def deletefromcart(product_id):
    product = Cart.query.filter_by(product_id = product_id, user_id = current_user.id).first()
    db.session.delete(product)
    db.session.commit()
    flash('Product has been removed', 'success')
    return redirect(url_for('cart'))


@main.route('/deleteallfromcart', methods=['GET'])
@login_required
def deleteallfromcart():
    db.session.query(Cart).filter(Cart.user_id == current_user.id).delete()
    db.session.commit()
    flash('All products have been removed', 'success')
    return redirect(url_for('index'))






 #if user and current_user.email != user.email:

    
       