'''Get a correctly formatted calendar'''
from datetime import datetime, timedelta
import calendar
MONTHS = ['January', 'February', 'March','April','May','June','July','August','September','October','November','December']
class Cal():
    '''static class for working with dates'''
    def get_month(month=None, year=None):
        '''get the view model for a month/year'''
        #if our params are None, set them to today's values
        if month is None:
            month = datetime.today().month
        if year is None:
            year = datetime.today().year
        print('get month', month, year)
        #get our calendar instance
        c = calendar.Calendar(calendar.SUNDAY)
        #to collect our days
        days = list()
        #loop over the dates in this month
        for day in c.itermonthdates(year, month):
            #convert the dow to my system
            dow = Cal._get_dow(day.weekday())
            #add any empty days needed
            if day.month != month:
                days.append(Day(dow))
                #continue early
                continue
            days.append(Day(dow, day.day))
        current_month = Month(month, Cal._get_month_name(month), year)
        if month == 12:
            next_month = Month(1, Cal._get_month_name(1), year + 1)
            last_month = Month(month - 1, Cal._get_month_name(month - 1), year)
        elif month == 1:
            month_number = 12
            next_month = Month(month + 1, Cal._get_month_name(month + 1), year)
            last_month = Month(month_number, Cal._get_month_name(12), year -1)
        else:
            next_month_number = month + 1
            last_month_number = month - 1
            last_month = Month(last_month_number, Cal._get_month_name(last_month_number), year)
            next_month = Month(next_month_number, Cal._get_month_name(next_month_number), year)
        print('next month', next_month.number, next_month.name, next_month.year)
        print('last month', last_month.number, last_month.name, last_month.year)
        return MonthViewModel(days,\
        this_month=current_month, next_month=next_month,\
        last_month=last_month, year_number=year, month_number=month)
    def get_days_betwen(start, end):
        '''get day object between two dates passed in as text 01-01-1970'''
        start_arr = list(map(int, start.split('-')))
        end_arr = list(map(int, end.split('-')))
        start_date = datetime(year=start_arr[2], month=start_arr[0], day=start_arr[1])
        end_date = datetime(year=end_arr[2], month=end_arr[0], day=end_arr[1])
        delta = end_date - start_date
        ret = list()
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            dow = Cal._get_dow(day.weekday())
            date_string = '{m}-{d}-{y}'.format(m=day.month, d=day.day, y=day.year)
            ret.append(Day(dow, day.day, date_string))
        return ret
    def _get_month_name(month):
        return MONTHS[month - 1]
    def _get_dow(dow):
        if dow == 6:
            return 0
        return dow + 1
class Day():
    def __init__(self, dow, day=None, date_string=None):
        self.dow = dow
        self.day = day
        self.date_string = date_string
    def to_dict(self):
        return {'dow': self.dow, 'day': self.day}
    def __repr__(self):
        format_string = '{d}'
        if self.dow == 0:
            format_string = 'sun {d}'
        elif self.dow == 1:
            format_string = 'mon {d}'
        elif self.dow == 2:
            format_string = 'tue {d}'
        elif self.dow == 3:
            format_string = 'wed {d}'
        elif self.dow == 4:
            format_string = 'thr {d}'
        elif self.dow == 5:
            format_string = 'fri {d}'
        elif self.dow == 6:
            format_string = 'sat {d}'
        else:
            print(self.dow)
            raise ValueError('weekday error')
        return format_string.format(d=self.day)

class MonthViewModel():
    def __init__(self, days, **kwargs):
        self.days = days
        self.this_month = kwargs['this_month']
        self.last_month = kwargs['last_month']
        self.next_month = kwargs['next_month']
        self.month_number = kwargs['month_number']
        self.year_number = kwargs['year_number']
    def to_dict(self):
        '''convert to dictionary'''
        m = dict()
        m['days'] = list(map(lambda d: d.to_dict(), self.days))
        m['this_month'] = self.this_month.to_dict()
        m['last_month'] = self.last_month.to_dict()
        m['next_month'] = self.next_month.to_dict()
        m['month_number'] = self.month_number
        m['year_number'] = self.year_number
        return m
class Month():
    def __init__(self, number, name, year):
        self.number = number
        self.name = name
        self.year = year
    def to_dict(self):
        return {'number': self.number, 'name': self.name, 'year': self.year}
if __name__ == '__main__':
    print(Cal.get_days_betwen('1-1-2017', '2-3-2017'))
