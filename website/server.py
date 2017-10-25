import time
from datetime import datetime
from functools import reduce
from flask import Flask, render_template, request, jsonify, redirect, session
from data.models import TimeOffRequest, RequestDay, User
from data.cal import Cal
from data.database import Database
DB = Database()

app = Flask(__name__, '/static', static_folder='static', template_folder='templates')
app.secret_key = 'war on tugs'
app.debug = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
@app.context_processor
def inject_user():
    if check_for_user():
        return dict(signed_in=True)
    return dict(signed_in=False)
@app.route('/sign_out')
def signout():
    del session['username']
    del session['expiration']
    return render_template('login.html')
@app.route('/', methods=['get'])
def index():
    '''main page for the application'''
    if check_for_user():
        print('user exists')
        user = DB.get_user(session['username'])
        pending_requests = list()
        approved_requests = list()
        complete_requests = list()
        hours_earned = reduce(lambda l, r: l + r.hours, user.employee.time_earned, 0)
        hours_requested = 0
        hours_taken = 0
        for r in user.employee.time_requested:
            if r.days[len(r.days) - 1].date < datetime.today():
                hours_taken = reduce(lambda l, r: l + r.hours, r.days, hours_taken)
                complete_requests.append(r)
            else:
                hours_requested = reduce(lambda l, r: l + r.hours, r.days, hours_requested)
                pending_requests.append(r)
        hours_remaining = hours_earned - (hours_requested + hours_taken)
        return render_template('index.html',\
        pending_requests=pending_requests,\
        approved_requests=approved_requests,\
        complete_requests=complete_requests,\
        hours_earned='{v:10.2f}'.format(v=hours_earned),\
        hours_requested='{v:10.2f}'.format(v=hours_requested),\
        hours_taken='{v:10.2f}'.format(v=hours_taken),\
        hours_remaining='{v:10.2f}'.format(v=hours_remaining))
    else:
        return redirect('/login')
@app.route('/login', methods=['get', 'post'])
def login():
    print('login')
    if check_for_user():
        return redirect('/')
    else:
        if request.method == 'GET':
            return render_template('login.html')
        else:
            username = request.form.get('username')
            if username is None:
                return render_template('login.html', message="error loging in")
            user = DB.get_user(username)
            if user is None:
                return render_template('login.html', message="error loging in")
            session['username'] = username
            session['expiration'] = time.time() + (30 * 60)
            return redirect('/')
@app.route('/new', methods=['get'])
def new():
    '''A new request for time off'''
    if not check_for_user():
        return redirect('/login')
    month = request.args.get('month')
    year = request.args.get('year')
    print('/calendar', month, year)
    c = Cal.get_month(_safe_parse(month), _safe_parse(year))
    return render_template('new.html', calendar=c)
@app.route('/calendar', methods=['get'])
def calendar():
    print('/calendar')
    if not check_for_user():
        return redirect('/login')
    month = request.args.get('month')
    year = request.args.get('year')
    c = Cal.get_month(_safe_parse(month), _safe_parse(year))
    return jsonify(c.to_dict())
@app.route('/hours', methods=['post'])
def hours():
    if not check_for_user():
        return redirect('/login')
    try:
        start = request.form.get('start-day')
        end = request.form.get('end-day')
        dates = Cal.get_days_betwen(start, end)
        return render_template('hours.html', dates=dates)
    except Exception as e:
        print('error', e)
        return redirect('/new')
@app.route('/submitRequest', methods=['get','post'])
def submit_request():
    if not check_for_user():
        return redirect('/login')
    days = list()
    for k in request.form:
        if k == 'note':
            note = request.form.get(k)
        else:
            date = Cal.parse_date(k)
            hours = int(request.form.get(k))
            days.append(RequestDay(date=date, hours=hours))
    user = get_user();
    pto = TimeOffRequest(note=note, days=days, employee_id=user.employee.employee_id)
    DB.add_requests(pto)
    return redirect('/')

@app.route('/admin', methods=['get'])
def admin():
    '''For system admins only'''
    if not check_for_user():
        return redirect('/login')
    if request.method == 'GET':
        return render_template('admin.html')
@app.route('/approve', methods=['get'])
def approve():
    '''for employee admins only'''
    if not check_for_user():
        return redirect('/login')
    if request.method == 'GET':
        return render_template('approve.html')
@app.template_filter('date_string')
def date_string(date_time):
    return '{m}-{d}-{y}'.format(m=date_time.month,\
    d=date_time.day, y=date_time.year)
@app.template_filter('dow')
def dow(day_number):
    if day_number == 0:
        return 'sun'
    elif day_number == 1:
        return 'mon'
    elif day_number == 2:
        return 'tue'
    elif day_number == 3:
        return 'wed'
    elif day_number == 4:
        return 'thur'
    elif day_number == 5:
        return 'fri'
    elif day_number ==6:
        return 'sat'
def get_user():
    return DB.get_user(session['username'])
def _safe_parse(text):
    if text is None:
        return None
    try:
        return int(text)
    except ValueError:
        return None

def check_for_user():
    try:
        session_username = session['username']
        #will throw a ValueError if not a number
        expiration = float(session['expiration'])
        #get the current time in seconds
        current = time.time()
        #if the login has expired
        if current > expiration:
            del session['username']
            del session['expiration']
            return False
    except Exception as e:
        return False
    return True
if __name__ == '__main__':
    app.run(debug=True)
