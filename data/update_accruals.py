from datetime import datetime, timedelta
from data.models import Accrual, Employee, Config
from data.database import Database
from data.cal import Cal
# If no PTO has been earned
# set the last pay date to two weeks ago
# this past friday
# If PTO has been earned
# get the last payout
# for each 2 week period
# between the last payout for this employee
# and the last payout for anyone
# add an accrual rate for each fortnight
def update_accruals():
    d = Database()
    session = d._get_session()
    config = session.query(Config)\
    .order_by(Config.year.desc())\
    .first()
    pay_days = calculate_year_paydates(config.pay_start, config.pay_interval)
    for emp in d.get_employees():
        if len(pay_days) > len(emp.time_earned):
            for day in pay_days[len(emp.time_earned)]:
                emp.time_earned.append(Accrual(pay_date=day,time_earned=emp.accrual_rate))
    session.commit()
def calculate_year_paydates(pay_start, pay_interval):
    ret = list()
    today = datetime.today()
    day = pay_start
    while pay_start < today:
        if pay_start.weekday() == 4:
            ret.append(day)
        day = day + timedelta(days=pay_interval)
    return ret