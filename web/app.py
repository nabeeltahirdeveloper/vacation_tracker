#!usr/bin/python3
"""
script to start a flask web application
"""

from models import storage, User, Employment
from flask import Flask, render_template, request, redirect
from flask_bcrypt import Bcrypt
import uuid
#from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from datetime import datetime, timedelta
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "1234"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://lynks_eng:lynks_eng_pwd@localhost/lynks_db'
# migrate = Migrate(app, db)

@login_manager.user_loader


@app.teardown_appcontext
def teardown(Exception):
    """
    remove the current SQLAlchemy Session
    """
    storage.close()

@app.route('/home', strict_slashes=False, methods=["GET"])
def home():
    """
    home
    """
    return render_template("home.html")

@app.route("/", strict_slashes=False, methods=["GET", "POST"])
@app.route("/login", strict_slashes=False, methods=["GET", "POST"])
def login():
    """
    Login
    """
    print(request.method)
    if request.method == "POST":
        
        email = request.form['email']
        password = request.form['password']
        
        print('email', email, password)
        
        user= storage.get_user_by_email(email)
        print('user', user)
        if user is None:
            return redirect('/login')
        
        check = bcrypt.check_password_hash(user.password, password)
        print('check', check)
        if check:
            login_user(user)
            if user.user_role == 'Super Admin' or user.user_role == 'Admin':
                return redirect('/dashboard')
            return redirect('/user_dashboard')
        
        return redirect('/login')
        
        
    else:    
    
        return render_template("login.html")




@app.route("/user_dashboard", strict_slashes=False, methods=["GET", "POST"])
@login_required
def user_dashboard():
    """
    user_dashboard
    """
    
    user = current_user
    
    userEmployement = storage.get_employment_by_user_id(user.id)
    startDate = userEmployement.starts_at
    format_start_date = datetime.strptime(str(startDate), "%Y-%m-%d %H:%M:%S").date()
    print('startDate', format_start_date)
    todayDate= datetime.today().date()
    three_months_before = todayDate - timedelta(days=90)
    print("format_start_date < three_months_before", format_start_date < three_months_before, three_months_before, format_start_date)
    if format_start_date > three_months_before:
        balance = 0
    else: 
        balance = 21
    
    return render_template("user_dashboard.html", balance=balance, fname=user.first_name, lname=user.last_name)


@login_manager.user_loader
def load_user(user_email):
    return storage.get_user_by_email(user_email)




@app.route("/dashboard", strict_slashes=False, methods=["GET", "POST"])
# @login_required
def dashboard():
    """
    users
    """
    
    print('current user', storage.count(User))
    # if current_user.user_role == 'Super Admin' or current_user.user_role == 'Admin':
    return render_template(
        "dashboard.html",
        users=storage.all(User),
        name=type(storage.all(User)),
        cache_id=uuid.uuid4(),
        user_count=storage.count(User)
    )
    # elif current_user.user_role == 'User':
    #     return redirect('/user_dashboard')
    
    # return render_template(
    #     "dashboard.html",
    #     users=storage.all(User),
    #     name=type(storage.all(User)),
    #     cache_id=uuid.uuid4()
    # )
    
@app.route("/logout", strict_slashes=False, methods=["GET", "POST"])
@login_required
def logout():
    """
    logout
    """
    logout_user()
    return redirect('/login')

@app.route("/about", methods=["GET", "POST"])
def about():
    """
    about
    """
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    """
    contact
    """
    return render_template("contact.html")
@app.route("/register", strict_slashes=False, methods=["GET", "POST"])
def register():
    title=request.form["title"]
    fname=request.form["fname"]
    lname=request.form["sname"]
    email = request.form['email']
    password1 = request.form['password']
    email2=request.form['personal_email']
    user_role=request.form['user_role']
    national_id=request.form['National_ID_Number']
    phone=request.form['Phone']
    personal_phone=request.form['Personal_Phone']
    title=request.form['title']
    unit_id=request.form['Unit_ID']
    addr=request.form['addr']
    
    hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
    
    entry=User(
        title=title,
        first_name=fname,
        last_name=lname,
        email=email,
        password=hashed_password,
        personal_email=email2,
        user_role=user_role,
        national_id_number=national_id,
        personal_phone=personal_phone,
        phone=phone,
        unit_id=unit_id
    )
    storage.new(entry)
    
    employment_entry = Employment(
        starts_at= datetime.now(),
        user_id=entry.id
    )
    
    
    storage.new(employment_entry)
    
    
    storage.save()
    return redirect('/dashboard')



@app.route("/forgot-password", strict_slashes=False, methods=["GET", "POST"])
def forgot_password():
    """
    forgot-password
    """
    return render_template("forgot-password.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
