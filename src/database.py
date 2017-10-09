'''data access layer'''
import sqlite3
import datetime
from sqlalchemy import Table, Column, MetaData,\
create_engine, Integer, String, Boolean, DateTime,\
Float, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker, relationship
from src.models import Employee, RequestedTime, EarnedTime

class Database():
    '''Database interface'''
    def __init__(self, conn_str='sqlite:///pto.sqlite'):
        self.engine = create_engine(conn_str)
        self.metadata = MetaData(bind=self.engine)
        self.earned_time = self._map_earned_time()
        self.requested_time = self._map_requested_time()
        self.employees = self._map_employee()
        self.metadata.create_all()
    def get_employees(self):
        pass
    def add_employee(self, employee):
        '''add a new employee'''
        try:
            session = self._get_session()
            session.add(employee)
            session.commit()
            return True
        except:
            return False
    def add_earned(self, earned_time):
        '''add hours earned'''
        try:
            session = self._get_session()
            session.add(earned_time)
            session.commit()
            return True
        except:
            return False
    def add_requested(self, request):
        '''add new request for pto'''
        try:
            session = self._get_session()
            session.add(request)
            session.commit()
            return True
        except:
            return False
    def _get_session(self):
        session = sessionmaker(bind=self.engine)
        return session()
    def _map_employee(self):
        t = Table('employees', self.metadata,\
        Column('id', Integer, primary_key=True),\
        Column('first_name', String),\
        Column('last_name', String),\
        Column('hire_date', DateTime),\
        Column('pto_earned', Float))
        mapper(Employee, t, properties={
            'earned_time': relationship(EarnedTime,backref='employees'),
            'requested_time': relationship(RequestedTime, backref='employees')
        })
        return t
    def _map_earned_time(self):
        t = Table('earned_time', self.metadata,\
        Column('id', Integer, primary_key=True),\
        Column('employee_id', Integer, ForeignKey('employees.id')),\
        Column('week_earned', Integer),\
        Column('hours', Float))
        mapper(EarnedTime,t)
        return t
    def _map_requested_time(self):
        t = Table('requested_time', self.metadata,\
        Column('id', Integer, primary_key=True),\
        Column('employee_id', Integer, ForeignKey('employees.id')),\
        Column('hours', Float),\
        Column('hours', Float))
        mapper(RequestedTime, t)
        return t