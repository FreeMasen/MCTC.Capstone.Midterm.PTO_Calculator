'''data access layer'''
from datetime import date, timedelta, datetime
from sqlalchemy import Table, Column, MetaData, create_engine
from sqlalchemy.orm import mapper, sessionmaker, relationship
from data.models import Employee, TimeOffRequest, Accrual, User, Base
import bcrypt
class Database():
    '''Database interface'''
    def __init__(self, conn_str='sqlite:///pto.sqlite'):
        self.engine = create_engine(conn_str)
        Base.metadata.create_all(self.engine)
    def get_employees(self):
        '''get full list of employees'''
        try:
            session = self._get_session()
            return session.query(Employee).join(User, Employee.employee_id == User.employee_id).all()
        except:
            return list()
    def get_employee(self, employee_id):
        '''get a single employee'''
        pass
    def get_user(self, username):
        '''get a single user'''
        print('get_user', username)
        try:
            session = self._get_session()
            users = session.query(User).filter(User.username == username).all()
            print(users)
            return users[0]
        except Exception as e:
            print(e)
            return None
    def get_requests(self, employee_id):
        '''get a list of requests for this employee'''
        pass
    def get_timeoff(self, employee_id):
        '''get a list of accrued time off for an employee'''
        pass
    def add_employee(self, employee):
        '''add a new employee'''
        try:
            session = self._get_session()
            session.add(employee)
            session.add(employee.user)
            session.commit()
            return True
        except Exception as e:
            print(e)
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
    def add_request(self, user):
        '''add new request for pto'''
        try:
            session = self._get_session()
            session.update(user)
            session.update(user.employee)
            session.update(user.employee.time_requested)
            session.commit()
            return True
        except:
            return False
    def add_requests(self, requests):
        try:
            session = self._get_session()
            session.add(requests)
            session.commit()
            return True
        except:
            return False
    def delete_users(self, employee_ids):
        try:
            print('delete_users', employee_ids)
            session = self._get_session()
            for eid in employee_ids:
                session.query(User).filter(User.employee_id == eid).delete()
                session.query(Employee).filter(Employee.employee_id == eid).delete()
            session.commit()
        except Exception as e:
            print(e)
            return False
    def update_user_roles(self, changes):
        print('database->update_user_roles', changes)
        try:
            session = self._get_session()
            for change in changes:
                query = session.query(User).filter(User.employee_id == change['empId'])
                if change['checked']:
                    query.update({User.roles: User.roles + change['role']})
                else:
                    list(filter(lambda r: r != change['role'], User.roles))
                    query.update({User.roles: list(filter(lambda r: r != change['role'], User.roles))})
            session.commit()
            print('update_user_roles complete')
        except Exception as e:
            print('update_user_roles error', e)

    def _get_session(self):
        session = sessionmaker(bind=self.engine)
        return session()

if __name__ == '__main__':
    pass

