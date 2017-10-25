if __name__ == '__main__':
    from data.models import Employee, Accrual, TimeOffRequest, RequestDay, Roles, User
    from data.database import Database
    import bcrypt
    from datetime import datetime
    d = Database()
    pw = bcrypt.hashpw('timeoff', bcrypt.gensalt(15))
    user = User(username='admin', password_hash=pw, roles=['user', 'approver', 'admin'])
    employee = Employee(first_name='admin', last_name='admin', hire_date=datetime(year=1970, month=1, day=1), user=user)
    d.add_employee(employee)
