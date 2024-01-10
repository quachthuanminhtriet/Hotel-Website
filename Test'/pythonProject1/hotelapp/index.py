from flask import render_template, request, redirect, url_for, jsonify, session
from hotelapp import app, dao, login, utils
from hotelapp.admin import *
import math
from flask_login import login_user, logout_user


# Trang chủ
@app.route("/")
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')

    rooms = dao.get_rooms(kw, cate_id, page)

    num = dao.count_rooms()
    page_size = app.config['PAGE_SIZE']

    return render_template('index.html',
                           rooms=rooms, pages=math.ceil(num / page_size))


#  lấy id user login
@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


# admin login
@app.route("/admin/login", methods=['post'])
def login_admin():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


# context processor để chia sẻ dữ liệu chung với tất cả các template
@app.context_processor
def common_responses():
    return {
        'typeofrooms': dao.get_type_of_rooms(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }


# chuyển trang detail dựa trên id
@app.route('/rooms/<id>')
def details(id):
    return render_template('detail.html',
                           rooms=dao.get_rooms_by_id(id),
                           room=dao.get_room())


@app.route("/cart")
def cart():
    return render_template('cart.html')


@app.route("/api/cart", methods=['post'])
def add_to_cart():
    data = request.json

    cart = session.get('cart')
    if cart is None:
        cart = {}

    id = str(data.get("id"))
    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }

    session['cart'] = cart

    """
        {
            "1": {
                "id": "1",
                "name": "...",
                "price": 123,
                "quantity": 2
            },  "2": {
                "id": "2",
                "name": "...",
                "price": 1234,
                "quantity": 1
            }
        }
    """

    return jsonify(utils.count_cart(cart))


@app.route("/api/cart/<rooms_id>", methods=['put'])
def update_cart(rooms_id):
    cart = session.get('cart')
    if cart and rooms_id in cart:
        quantity = request.json.get('quantity')
        cart[rooms_id]['quantity'] = int(quantity)

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.route("/api/cart/<rooms_id>", methods=['delete'])
def delete_cart(rooms_id):
    cart = session.get('cart')
    if cart and rooms_id in cart:
        del cart[rooms_id]

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.route('/api/pay', methods=['post'])
def pay():
    try:
        dao.add_receipt(session.get('cart'))
    except:
        return jsonify({'status': 500, 'err_msg': "Some thing wrong"})
    else:
        del session['cart']
        return jsonify({'status': 200})


if __name__ == "__main__":
    from hotelapp import admin

    app.run(debug=True)
