from hotelapp.models import Rooms, User, TypeOfRooms
from hotelapp import app, db
import hashlib
from sqlalchemy import func


def get_type_of_rooms():
    return TypeOfRooms.query.all()


def get_rooms(kw, cate_id, page):
    rooms = Rooms.query

    if kw:
        rooms = rooms.filter(Rooms.name.contains(kw))

    if cate_id:
        rooms = rooms.filter(Rooms.typeofrooms_id.__eq__(cate_id))

    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size

        return rooms.slice(start, start + page_size)

    return rooms.all()


def get_room():
    return Rooms.query.all()


def count_rooms():
    return Rooms.query.count()


def count_rooms_by_cate():
    return db.session.query(TypeOfRooms.id, TypeOfRooms.name, func.count(Rooms.id)) \
        .join(Rooms, Rooms.typeofrooms_id.__eq__(TypeOfRooms.id), isouter=True) \
        .group_by(TypeOfRooms.id).all()


def get_rooms_by_id(id):
    return Rooms.query.get(id)


def get_user_by_id(account_id):
    return User.query.get(account_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password)).first()
