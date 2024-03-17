#!usr/bin/python3
"""
script to start a flask web application
"""

from models import storage, User, Employment, LeaveRequest
from flask import Flask, render_template, request, redirect, flash
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



@app.route('/apply-leave', strict_slashes=False, methods=["GET", "POST"])
@login_required
def apply_leave():
    """
    apply_leave
    """
    user = current_user
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    number_of_days = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
    print('number_of_days', number_of_days)
    
    userEmployement = storage.get_employment_by_user_id(user.id)
    startDate = userEmployement.starts_at
    format_start_date = datetime.strptime(str(startDate), "%Y-%m-%d %H:%M:%S").date()
    print('startDate', format_start_date)
    todayDate= datetime.today().date()
    three_months_before = todayDate - timedelta(days=90)
    print("format_start_date < three_months_before", format_start_date < three_months_before, three_months_before, format_start_date)
    if format_start_date > three_months_before:
        flash('You are not eligible to apply for leave')
        return redirect('/home')
    


    if int(user.yearly_leave) == 0:
        flash('You have no leave days left')
        return redirect('/home')
    
    elif int(user.yearly_leave) > 0:

        yearly_leave = int(user.yearly_leave)
        yearly_leave -= number_of_days
        if yearly_leave < 0:
            flash('You have no enough leave days left')
            return redirect('/user_dashboard')
        user.yearly_leave = yearly_leave
        storage.save()

    
        return redirect('/user_dashboard')

    
    




@app.route("/user_dashboard", strict_slashes=False, methods=["GET", "POST"])
@login_required
def user_dashboard():
    """
    user_dashboard
    """
    
    user = current_user
    userId = user.id
    print(userId)

    userLeaves = storage.get_leaves_requests_by_user_id(userId)
    print("userLeaves", userLeaves)
    userEmployement = storage.get_employment_by_user_id(user.id)
    startDate = userEmployement.starts_at
    format_start_date = datetime.strptime(str(startDate), "%Y-%m-%d %H:%M:%S").date()
    print('startDate', format_start_date)
    todayDate= datetime.today().date()
    three_months_before = todayDate - timedelta(days=90)
    print("format_start_date < three_months_before", format_start_date < three_months_before, three_months_before, format_start_date)
    if format_start_date > three_months_before:
        balance = 0
        current_balance = 0
    else: 
        balance = 21
        current_balance = user.yearly_leave
    
    return render_template("user_dashboard.html",current_balance=current_balance, balance=balance, fname=user.first_name, lname=user.last_name, userLeaves=userLeaves)



@app.route("/manager_dashboard", strict_slashes=False, methods=["GET", "POST"])
@login_required
def manager_dashboard():
    """
    user_dashboard
    """
    
    user = current_user
    userId = user.id
    print(userId)

    managerLeaves = storage.get_leaves_requests_by_manager_id(userId)
    print("managerLeaves", managerLeaves)

    for leave in managerLeaves:
        user = storage.get_user_by_id(leave.user_id)
        leave.email = user.email
    
    return render_template("manager_dashboard.html", fname=user.first_name, lname=user.last_name, managerLeaves=managerLeaves)


@app.route("/approve-leave", strict_slashes=False, methods=["GET", "POST"])
@login_required
def approve_leave():
    """
    approve_leave
    """
    user = current_user
    leave_id = request.form['requestId']
    leave = storage.get(LeaveRequest, leave_id)
    leave_user = storage.get_user_by_id(leave.user_id)
    leave.status = 'approved'
    yearly_leave = int(leave_user.yearly_leave)
    yearly_leave -= int(leave.leave_days)
    leave_user.yearly_leave = yearly_leave
    storage.save()
    return redirect('/manager_dashboard')


@app.route("/reject-leave", strict_slashes=False, methods=["GET", "POST"])
@login_required
def reject_leave():
    """
    reject_leave
    """
    user = current_user
    leave_id = request.form['requestId']
    leave = storage.get(LeaveRequest, leave_id)
    leave.status = 'rejected'
    storage.save()
    return redirect('/manager_dashboard')


@login_manager.user_loader
def load_user(user_email):
    return storage.get_user_by_email(user_email)



@app.route("/apply-for-leave", strict_slashes=False, methods=["GET", "POST"])
@login_required
def apply_for_leave():
    """
    apply_for_leave
    """
    user = current_user
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    number_of_days = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
    print('number_of_days', number_of_days)
    
    userEmployement = storage.get_employment_by_user_id(user.id)
    startDate = userEmployement.starts_at
    format_start_date = datetime.strptime(str(startDate), "%Y-%m-%d %H:%M:%S").date()
    print('startDate', format_start_date)
    todayDate= datetime.today().date()
    three_months_before = todayDate - timedelta(days=90)
    print("format_start_date < three_months_before", format_start_date < three_months_before, three_months_before, format_start_date)
    if format_start_date > three_months_before:
        flash('You are not eligible to apply for leave')
        return redirect('/home')
    


    if int(user.yearly_leave) == 0:
        flash('You have no leave days left')
        return redirect('/home')
    
    elif int(user.yearly_leave) > 0:

        yearly_leave = int(user.yearly_leave)
        yearly_leave -= number_of_days
        if yearly_leave < 0:
            flash('You have no enough leave days left')
            return redirect('/user_dashboard')
        
        entry = LeaveRequest(
            user_id=user.id,
            start_date=start_date,
            end_date=end_date,
            status='pending',
            leave_days=number_of_days,
            manager_id=user.head_user_id
        )
        storage.new(entry)
        storage.save()
        


        flash('Leave request sent successfully')
        return redirect('/user_dashboard')






@app.route("/dashboard", strict_slashes=False, methods=["GET", "POST"])
@login_required
def dashboard():
    """
    users
    """
    print('current user', storage.count(User))
    if current_user.user_role == 'Super Admin':
        users = storage.all(User)
        users = list(users.values())
        for user in users:
            print("user", user)
            user.unit_name = storage.get_unit_id_by_id(user.unit_id).name
        return render_template(
            "dashboard.html",
            users=storage.all(User),
            name=type(storage.all(User)),
            cache_id=uuid.uuid4(),
            user_count=storage.count(User)
        )
    elif current_user.user_role == 'User':
        return redirect('/user_dashboard')
    elif current_user.user_role == 'Admin':
        return redirect('/manager_dashboard')
    
    return render_template(
        "dashboard.html",
        users=storage.all(User),
        name=type(storage.all(User)),
        cache_id=uuid.uuid4()
    )

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
    headUser=request.form['Head_User_ID']
    
    hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')

    unit_data = storage.get_unit_id_by_name(unit_id)
    if unit_data is None:
        return redirect('/register')
    print('unit_data', unit_data)

    
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
        unit_id=unit_data.id,
        head_user_id=headUser
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
