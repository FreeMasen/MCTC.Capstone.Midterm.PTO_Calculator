'''Get a correctly formatted calendar'''
from datetime import datetime
import calendar
class Cal():
    def get_month(month, year):
        c = calendar.Calendar(calendar.SUNDAY)
        ret = list()
        last_dow = 0
        for day in c.itermonthdates(year, month):
            #convert the dow to my system
            dow = Cal._get_dow(day.weekday())
            #add any empty days needed
            if day.month != month:
                ret.append(Day(dow))
                #continue early
                continue
            ret.append(Day(dow, day.day))
        return ret
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
if __name__ == '__main__':
    for i in range(12):
        print(i + 1)
        month = Cal.get_month(i + 1, 2017)
        for day in month:
            print(day)
