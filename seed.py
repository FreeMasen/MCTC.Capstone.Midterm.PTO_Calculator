
if __name__ == '__main__':
    import bcrypt
    from data.models import Employee, User
    from data.database import Database
    from datetime import datetime
    d = Database()
    password = bcrypt.hashpw('freetime', bcrypt.gensalt(15))
    user = User(username='admin',\
    password_hash=password,\
    roles=['user', 'approver', 'admin'])
    emp = Employee(user=user,\
    first_name='admin',\
    last_name='admin',\
    accrual_rate=5.16,
    hire_date=datetime(year=1970, month=1, day=1))
    d.add_employee(emp)
