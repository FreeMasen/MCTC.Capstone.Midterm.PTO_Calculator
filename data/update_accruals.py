from datetime import datetime, timedelta
from data.models import Accrual, Employee
from data.database import Database
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
    last_payday = get_last_payday()
    d = Database()
    session = d._get_session()
    for emp in d.get_employees():
        if len(emp.time_earned) < 1:
            
                this_friday = get_this_friday()
                next_pay_day = this_friday + timedelta(days=14)
                emp.time_earned.append(Accrual(pay_date=\
                next_pay_day,hours=emp.accrual_rate))
        else
            last_earned = emp.time_earned[-1]
            delta = last_earned.pay_date - datetime.today()
            last_day_earned = abs(delta.days)
            if last_day_earned >= 14:
                emp.time_earned.append(Accrual(pay_date=\
                last_day_earned + timedelta(days=14),\
                hours=emp.accrual_rate))
                session.add(emp)
    session.commit()

def get_last_payday():
    d = Database()
    session = d._get_session()

    last_pay_day = session.query(Accrual).\
    order_by(Accrual.pay_date.desc()).first()
    if last_pay_day is None:
        friday = get_this_friday()
        return friday - timedelta(days=14)

def get_this_friday():
    today = datetime.today()
    while (today.weekday() != 4):
        today += timedelta(days=1)
    return today