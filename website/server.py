from flask import Flask, render_template, request
from data.models import RequestedTime, RequestDay
from data.cal import Cal
app = Flask(__name__, '/static', static_folder='static', template_folder='templates')
app.debug = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
@app.route('/', methods=['get'])
def index():
    '''main page for the application'''
    pending_requests,\
    approved_requests,\
    complete_requests = mocks()

    return render_template('index.html',\
    pending_requests=pending_requests,\
    approved_requests=approved_requests,\
    complete_requests=complete_requests)

@app.route('/new', methods=['get', 'post'])
def new():
    '''A new request for time off'''
    if request.method == 'GET':
        c = Cal.get_month(10,2017)
        print('cal', c)
        return render_template('new.html', calendar=c)
@app.route('/admin', methods=['get'])
def admin():
    '''For system admins only'''
    if request.method == 'GET':
        return render_template('admin.html')
@app.route('/approve', methods=['get'])
def approve():
    '''for employee admins only'''
    if request.method == 'GET':
        return render_template('approve.html')

def mocks():
    pending_requests = list()
    pending_requests.append(RequestedTime('10/11/2017', 1,\
    'Beth\'s Birthday', [RequestDay('12/11/2017', 8), \
    RequestDay('12/12/2017', 8)]))
    pending_requests.append(RequestedTime('10/15/2017', 1, 'Thanksgiving',\
    [RequestDay('11/22/2017', 8), RequestDay('11/24/2017', 8)]))
    approved_requests = list()
    first_approved = RequestedTime('1/1/2017',1,'france',\
    [RequestDay('1/31/2017', 8),\
    RequestDay('2/1/2017', 8),\
    RequestDay('2/2/2017', 8),\
    RequestDay('2/3/2017', 8),\
    RequestDay('2/4/2017', 8)])
    first_approved.approved = True
    first_approved.approved_by = 'rmasen'
    first_approved.approved_date = '1/2/2017'
    approved_requests.append(first_approved)
    second_approved = RequestedTime('2/10/2017', 1, 'House Closing',\
    [RequestDay('2/18/2017', 8)])
    second_approved.approved = True,
    second_approved.approved_by = 'rmasen'
    second_approved.approved_date = '2/11/2017'
    approved_requests.append(second_approved)
    first_complete = RequestedTime('2/28/2017', 1, 'Fourth of July',\
    [RequestDay('7/5/2017', 8)])
    first_complete.approved = True
    first_complete.approved_by = 'rmasen'
    first_complete.approved_date = '3/5/2017'
    second_complete = RequestedTime('2/28/2017', 1, 'May Day',\
    [RequestDay('5/1/2017', 8)])
    second_complete.approved = True
    second_complete.approved_date = '4/20/2017'
    second_complete.approved_by = 'rmasen'
    complete_requests = [first_complete, second_complete]
    return (pending_requests, approved_requests, complete_requests)
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
if __name__ == '__main__':
    app.run(debug=True)
