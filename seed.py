
if __name__ == '__main__':
    import bcrypt
    from data.models import Employee, User, Config
    from data.database import Database
    from datetime import datetime, timedelta
    import json
    import io
    d = Database()
    def add_admin_user():
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
    def add_configs():
        session = d._get_session()
        db_config = session.query(Config).order_by(Config.year.desc()).first()
        this_year = datetime.today().year
        try:
            config_file = open('config.json')
            config = json.load(config_file)
        except:
            config = dict()
        if db_config == None or db_config.year < this_year:
            new_config = Config()
            new_config.pay_interval = \
            get_index_fallback(config, 'pay_interval', 14)
            new_config.first_payday = \
            get_index_fallback(config, 'first_payday', get_second_friday(this_year))
            new_config.default_password = \
            get_index_fallback(config, 'default_password', 'freetime')

    def get_index_fallback(dict, index, fallback):
        if dict[index] is None:
            return fallback
        return dict[index]

    def get_second_friday(year):
        day = datetime(year=year, month=1, day=1)
        friday_count = 0
        while friday_count < 2:
            if day.weekday() == 4:
                friday_count += 1
        return day