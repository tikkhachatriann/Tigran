import bleach
from flask import render_template, request, redirect, url_for
from flask_login import  login_user, current_user, logout_user, login_required

from app import app
from app.user import User
from app.utils import send_email
from app.main import UserController, BookingController


@app.route('/')
def home():
    return render_template('home.html')


@app.route("/contact_info", methods=["POST", "GET"])
def contact_info():
    if request.method == "GET":
        return render_template("contact_info.html")
    return render_template(
        "events_calendar.html",
        events=BookingController().get_events()
        )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':   
        return render_template("register.html")
    
    user_ctrl = UserController()
    form_data = request.form.to_dict()
    try:
        user_ctrl.register_user(request.form)
        return render_template("register_success.html")
    except Exception as ex:
        return render_template(
                "register.html", 
                error_message=ex,
                **form_data
        )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        logout_user()
        return render_template('login.html')
    
    user_ctrl = UserController()

    user_name = request.form["username"]
    password = request.form["password"]
    user_name = bleach.clean(user_name)

    user_data = user_ctrl.get_user(user_name)
    
    if not (user_data and user_ctrl.check_password(password, user_data[5])):
        return render_template(
            'login.html',
            error_message="*Invalid username or password.Please try again.",
            username=user_name
        )
    user = User(user_data[0])
    login_user(user)
    
    if current_user.is_authenticated:
        return redirect(url_for('events_calendar'))
    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/events_calendar', methods=["GET"])
@login_required
def events_calendar():
    if request.method == "GET":
        return render_template(
            'events_calendar.html', 
            events=BookingController().get_events()
        )
    
    
@app.route('/get_reserve_modal/<event_id>')
def get_modal_content(event_id):
    booking_ctrl = BookingController()
    event_data = booking_ctrl.get_events(event_id)

    if event_data and event_data['table_id_list']:
        table_id_list = [
            int(id_str) for id_str in event_data['table_id_list'].split(',')
        ]
    else:
        table_id_list = []
    return render_template(
            'reserve_tables.html',
            tables=booking_ctrl.get_tables(),
            date=event_data["date"],
            table_id_list=table_id_list
    )


@app.route("/get_time_modal/<table_id>")
def get_time_modal_content(table_id):
    return render_template(
        "time_choice.html",
        tableId=table_id
    )


@app.route('/get_booking_data')
def get_booking_data():
    booking_data = request.args
   
    table_id = booking_data["tableId"]
    event_id = booking_data["eventId"]

    BookingController().book_table(table_id, event_id)
    send_email(booking_data)
    return render_template(
        "booking_success.html",
        date=booking_data['date'],
        time=booking_data['time'],
        guests=booking_data['guests']
    )
    

@app.route('/qr_info', methods=['GET'])
def qr_info():
    return render_template(
        'qr_info.html', 
        booking_info="Information about the booking will be shown here."
    )
                   