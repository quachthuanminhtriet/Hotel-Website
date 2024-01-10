import hashlib

from hotelapp.models import Rooms, User, UserRoleEnum, Customer, Staff
from hotelapp import db, admin
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask_admin import BaseView, expose, AdminIndexView
from flask import redirect, request
from flask_admin.form import Select2Field


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyStaffView(ModelView):
    column_list = ['id', 'name', 'cccd', 'birth_day', 'user_id']

    form_overrides = {'User': Select2Field}
    column_editable_list = ['name']
    edit_modal = True


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(MyStaffView(Staff, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))
