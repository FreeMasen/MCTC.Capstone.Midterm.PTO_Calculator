'''Get a correctly formatted calendar'''
from datetime import datetime
import calendar
class Cal():
    def get_month(month=None, year=None):
        if month is None:
            month = datetime.today().month
        if year is None:
            year = datetime.today().year
        c = calendar.Calendar(calendar.SUNDAY)
        days = list()
        print('getting days', month, year)
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
            last_month = Month(month - 1, Cal._get_month_name(month + 1), year)
            next_month = Month(month + 1, Cal._get_month_name(month - 1), year)
        return MonthViewModel(days, current_month, last_month, next_month, month)
    def _get_month_name(month):
        if month == 1:
            return 'January'
        if month == 2:
            return 'February'
        if month == 3:
            return 'March'
        if month == 4:
            return 'April'
        if month == 5:
            return 'May'
        if month == 6:
            return 'June'
        if month == 7:
            return 'July'
        if month == 8:
            return 'August'
        if month == 9:
            return 'September'
        if month == 10:
            return 'October'
        if month == 11:
            return 'November'
        if month == 12:
            return 'December'

    def _get_dow(dow):
        if dow == 6:
            return 0
        return dow + 1
class Day():
    def __init__(self, dow, day=None):
        self.dow = dow
        self.day = day
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
    def __init__(self, days, this_month, last_month, next_month, month):
        self.days = days
        self.this_month = this_month
        self.last_month = last_month
        self.next_month = next_month
        self.month_number = month

class Month():
    def __init__(self, number, name, year):
        self.number = number
        self.name = name
        self.year = year

if __name__ == '__main__':
    for i in range(12):
        print(i + 1)
        month = Cal.get_month(i + 1, 2017)
        for day in month:
            print(day)
