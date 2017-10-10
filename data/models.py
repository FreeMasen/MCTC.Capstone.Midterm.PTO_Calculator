'''POPO Models'''
class Employee(object):
    '''Someone who works here'''
    def __init__(self, first_name, last_name, hire_date, pto_earned, id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.hire_date = hire_date
        self.pto_earned = pto_earned
        self.time_earned = list()
        self.time_requested = list()
    def __repr__(self):
        return '{id}: {fn} {ln}\n----------\nhire date: {hd}\nPTO Earned each pay period: {pe}'\
        .format(id=self.id, fn=self.first_name, ln=self.last_name, hd=self.hire_date, pe=self.pto_earned)
class EarnedTime(object):
    '''Earned Paid Time Off'''
    def __init__(self, pay_date, hours, employee_id, id=None):
        self.pay_date = pay_date
        self.hours = hours
        self.employee_id = employee_id
        self.id = id
    def __repr__(self):
        return '{id}: {eid}\n----------\nhours earned: {he}\nweek_earned: {pd}'\
        .format(id=self.id, eid=self.employee_id,he=self.hours, pd=self.pay_date)

class RequestedTime(object):
    '''Time off requested'''
    def __init__(self, date_requested, hours, start, end, employee_id, consumed, note, id=None):
        self.date_requested = date_requested
        self.start = start
        self.end = end
        self.hours = hours
        self.employee_id = employee_id
        self.consumed = consumed
        self.note = note
        self.id = id
    def __repr__(self):
        taken = 'yes' if self.consumed else 'no'
        return '{id}: {eid}\n------------\nhours requested: {hr}\nwhen: {st}-{en}\ntaken: {t}'\
        .format(id=self.id, eid=self.employee_id, hr=self.hours, t=taken, st=self.start, en=self.end)

class User(object):
    def __init__(self, username, password_hash=None, roles=None,id=None):
        self.username = username
        self.password_hash = password_hash
        self.roles = roles
        self.id = id
    def __repr__(self):
        return '{id}: {un}\n----------\npassword: {pw}\nroles:{rs}'\
        .format(id=self.id, un=self.username, pw=('*' * len(self.password_hash)), rs=self.roles)

class Role(object):
    def __init__(self, name, id=None):
        self.name = name
        self.id = id
    def __repr__(self):
        return '{id}: {n}'.format(id=self.id, n=self.name)

class UserRoles(object):
    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id
    def __repr__(self):
        return '{ui}: {ri}'.format(ui=self.user_id, ri=self.role_id)