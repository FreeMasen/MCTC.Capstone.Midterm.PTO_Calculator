from flask import Flask, templating, redirect, render_template, session, request
app = Flask(__name__, '/static', static_folder='static', template_folder='templates')
app.debug = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
@app.route('/', methods=['get'])
def index():
    return render_template('index.html')
@app.route('/new', methods=['get', 'post'])
def new():
    if request.method == 'GET':
        return render_template('new.html')
@app.route('/admin', methods=['get'])
def admin():
    if request.method == 'GET':
        return render_template('admin.html')
@app.route('/approve', methods=['get'])
def approve():
    if request.method == 'GET':
        return render_template('approve.html')
if __name__ == '__main__':
    app.run(debug=True)