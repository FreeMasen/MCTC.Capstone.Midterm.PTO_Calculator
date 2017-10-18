'''POPO Models'''
class Employee(object):
    '''Someone who works here'''
    def __init__(self, first_name, last_name, hire_date):
        self.employee_id = None
        self.first_name = first_name
        self.last_name = last_name
        self.hire_date = hire_date
        self.pto_earned = 0
        self.time_earned = list()
        self.time_requested = list()

class EarnedTime(object):
    '''Earned Paid Time Off'''
    def __init__(self, pay_date, hours, employee_id, earned_id=None):
        self.pay_date = pay_date
        self.hours = hours
        self.employee_id = employee_id
        self.earned_id = earned_id

class RequestedTime(object):
    '''Time off requested'''
    def __init__(self, date_requested, employee_id, note, days):
        self.time_off_id = id
        self.date_requested = date_requested
        self.employee_id = employee_id
        self.consumed = False
        self.note = note
        self.days = days
        self.approved = False
        self.approved_by = None
        self.approved_date = None

class RequestDay(object):
    '''A single day in a PTO request'''
    def __init__(self, date, hours, day_id=None):
        self.day_id = day_id
        self.date = date
        self.hours = hours

class User(object):
    '''A user, can be joined with an employee'''
    def __init__(self, username, password_hash=None, roles=None, user_id=None, employee_id=None):
        self.username = username
        self.password_hash = password_hash
        self.roles = roles
        self.user_id = user_id
        self.employee_id = employee_id

class Role(object):
    '''Access definitions'''
    def __init__(self, name, role_id=None):
        self.name = name
        self.role_id = role_id

class UserRoles(object):
    '''Join table of user's in a role'''
    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id
