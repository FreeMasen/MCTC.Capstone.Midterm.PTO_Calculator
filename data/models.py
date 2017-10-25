'''POPO Models'''
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean, Enum
from sqlalchemy.orm import relationship
import sqlalchemy.types as types
Base = declarative_base()

class Employee(Base):
    '''Someone who works here'''
    __tablename__ = 'employee'
    employee_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    hire_date = Column(DateTime)
    time_earned = relationship('Accrual', uselist=True)
    time_requested = relationship('TimeOffRequest', uselist=True)
    user = relationship('User', uselist=False, back_populates='employee')

class Accrual(Base):
    '''Earned Paid Time Off'''
    __tablename__ = 'Accrual'
    accrual_id = Column(Integer, primary_key=True)
    pay_date = Column(DateTime)
    hours = Column(Float)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))

class TimeOffRequest(Base):
    '''a single request for time off'''
    __tablename__ = 'request'
    request_id = Column(Integer, primary_key=True)
    date_requested = Column(DateTime, default=datetime.date.today())
    note = Column(String)
    approved = Column(Boolean, default=False)
    approved_by = Column(String)
    approved_date = Column(DateTime)
    days = relationship('RequestDay', uselist=True)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))

class RequestDay(Base):
    '''A single day in a PTO request'''
    __tablename__ = 'day';
    day_id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    hours = Column(Float)
    request_id = Column(Integer, ForeignKey('request.request_id'))

class Roles(types.TypeDecorator):
    '''a user's list of roles'''
    impl = types.Integer
    def process_bind_param(self, value, dialect):
        ret = 0
        if value is None:
            return ret
        for role in value:
            if role == 'user':
                ret += 1
            if role == 'approver':
                ret += 2
            if role == 'admin':
                ret += 4
        return ret
    def process_result_value(self, value, dialect):
        ret = list()
        if value & 1 > 0:
            ret.append('user')
        if value & 2 > 0:
            ret.append('approver')
        if value & 4 > 0:
            ret.append('adimg')
        return ret

class User(Base):
    '''A user, can be joined with an employee'''
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    employee = relationship('Employee', back_populates='user')
    roles = Column(Roles)