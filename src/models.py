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
    def __init__(self, week_earned, hours, employee_id, id=None):
        self.week_earned = week_earned
        self.hours = hours
        self.employee_id = employee_id
        self.id = id
    def __repr__(self):
        return '{id}: {eid}\n----------\nhours earned: {he}\nweek_earned: {we}'\
        .format(id=self.id, eid=self.employee_id,he=self.hours, we=self.week_earned)
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