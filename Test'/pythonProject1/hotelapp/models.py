from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import enum
from hotelapp import db, app
from datetime import datetime
import hashlib


# Role User
class UserRoleEnum(enum.Enum):
    ADMIN = 1
    STAFF = 2
    CUSTOMER = 3


# db Account
class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dchyeg7pv/image/upload/v1704726291/account.jgp_olt4oj.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.CUSTOMER)
    customer_id = relationship('Customer', backref='User', lazy=True)
    staff_id = relationship('Staff', backref='User', lazy=True)
    room_rental = relationship('RoomRental', backref='User', lazy=True)


class TypeOfRooms(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    room = relationship('Rooms', backref='TypeOfRooms', lazy=True)


class Rooms(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    image_room = Column(String(100),
                        default='https://res.cloudinary.com/dchyeg7pv/image/upload/v1704726291/account.jgp_olt4oj.jpg')
    typeofrooms_id = Column(Integer, ForeignKey(TypeOfRooms.id), nullable=False)


class Address(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    customer_id = relationship('Customer', backref='Address', lazy=True)


class Phone(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_phone = Column(String(100), nullable=False)
    number = Column(String(12), unique=True, nullable=False)
    customer_id = relationship('Customer', backref='Phone', lazy=True)


class TypeOfCustomer(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    customer_id = relationship('Customer', backref='TypeOfCustomer', lazy=True)


class Customer(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    cccd = Column(String(12), nullable=False, unique=True)
    birth_day = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    address_id = Column(Integer, ForeignKey(Address.id), nullable=False)
    phone_id = Column(Integer, ForeignKey(Phone.id), nullable=False)
    typeofcustomer_id = Column(Integer, ForeignKey(TypeOfCustomer.id), nullable=False)


class Staff(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    cccd = Column(String(12), nullable=False, unique=True)
    birth_day = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)


class Receipt(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    rooms_id = Column(Integer, ForeignKey(Rooms.id), nullable=False)


class RoomRental(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        u = User(username='admin',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRoleEnum.ADMIN)

        st = Staff(name='Triet', cccd='123456789', birth_day='2003-05-07', user_id=1)
        db.session.add(st)
        db.session.add(u)
        db.session.commit()

        # db.drop_all()
