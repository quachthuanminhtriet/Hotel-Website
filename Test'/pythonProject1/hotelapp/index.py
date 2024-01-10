from flask import render_template, request, redirect, url_for
from hotelapp import app, dao, login
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
    }


# chuyển trang detail dựa trên id
@app.route('/rooms/<id>')
def details(id):
    return render_template('detail.html',
                           rooms=dao.get_rooms_by_id(id),
                           room=dao.get_room())


if __name__ == "__main__":
    from hotelapp import admin

    app.run(debug=True)
