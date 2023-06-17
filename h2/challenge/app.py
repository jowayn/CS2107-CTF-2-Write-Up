from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps
from os import getenv
from sqlalchemy import event

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = getenv('SECRET', 'NOT_THE_ACTUAL_FLASK_SECRET')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

DEFAULT_ADMIN_PASSWORD = getenv('ADMIN_PASSWORD', 'test_admin_password')
FLAG = getenv('FLAG', 'CS2107{this_is_not_the_flag}')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    accounts = db.relationship('Account', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"

@event.listens_for(User.__table__, 'after_create')
def insert_initial_admin(*args, **kwargs):
    hashed_password = bcrypt.generate_password_hash(DEFAULT_ADMIN_PASSWORD).decode('utf-8')
    user = User(username='admin', password=hashed_password)
    db.session.add(user)
    db.session.commit()

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Account('{self.name}', '{self.balance}')"

@event.listens_for(Account.__table__, 'after_create')
def insert_initial_account(*args, **kwargs):
    account = Account(name='All da money', balance=1000000000000, user_id=1)
    db.session.add(account)
    db.session.commit()

with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check username and password')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.filter_by(id=session['user_id']).first()
    accounts = Account.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', user=user, accounts=accounts)
    
@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/create_account', methods=['GET', 'POST'])
@login_required
def create_account():
    if request.method == 'POST':
        name = request.form['name']
        balance = 0
        account = Account(name=name, balance=balance, user_id=session['user_id'])
        db.session.add(account)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_account.html')

@app.route('/account/<int:id>')
@login_required
def account(id):
    account = Account.query.get_or_404(id)
    if account.user_id != session['user_id']:
        return redirect(url_for('dashboard'))
    return render_template('account.html', account=account)

@app.route('/transfer/<int:id>', methods=['GET', 'POST'])
@login_required
def transfer(id):
    account = Account.query.get_or_404(id)
    if account.user_id != session['user_id']:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        if account.balance < float(request.form['amount']):
            flash('Insufficient funds')
            return redirect(url_for('transfer', id=id))
        if float(request.form['amount']) < 0:
            flash('Invalid amount')
            return redirect(url_for('transfer', id=id))
        account.balance -= float(request.form['amount'])
        account = Account.query.get_or_404(request.form['account'])
        account.balance += float(request.form['amount'])
        db.session.commit()
        return redirect(url_for('dashboard'))
    accounts = Account.query.filter_by(user_id=session['user_id']).all()
    return render_template('transfer.html', account=account, accounts=accounts)

@app.route('/super_vip_portal')
@login_required
def super_vip_portal():
    accounts = Account.query.filter_by(user_id=session['user_id']).all()
    if sum([account.balance for account in accounts]) < 100000000:
        return redirect(url_for('dashboard'))
    return render_template('super_vip_portal.html', flag=FLAG)

if __name__ == '__main__':
    app.run(debug=True)
