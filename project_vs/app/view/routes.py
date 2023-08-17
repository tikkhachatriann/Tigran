from sqlite3 import IntegrityError
from flask import render_template, request, redirect, url_for, session

from app import app
from app.utils import send_booking_confirmation_email
from app.database import get_db
from app.main import UserControler, BookingControler


class Table:
    def __init__(self, id, booked):
        self.id = id
        self.booked = booked
       

tables_data = [
    {"id": 1, "booked": False},
    {"id": 2, "booked": True},
    {"id": 3, "booked": False},
    {"id": 4, "booked": True},
    {"id": 5, "booked": True}
]

tables = [Table(**data) for data in tables_data]

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return  render_template('login.html')
    
    user_hadnler = UserControler()

    user_name = request.form["usrnm"]
    password = request.form["psw"]

    user_data = user_hadnler.is_user_valid(user_name)
    
    if not user_data or not user_hadnler.check_password(password, user_data[0]):
        return render_template(
            'login.html',
            error_message="*Invalid username or password. Please try again."
        )
    
    return redirect(url_for("events_calendar"))
        

@app.route('/events_calendar', methods = ["GET","POST"])
def events_calendar():
    events = [
        {"week_day": "TUE.", "date": "08.08", "dj_name": "DRRED"},
        {"week_day": "WED.", "date": "09.08", "dj_name": "ALENHERTZ"},
        {"week_day": "THU.", "date": "10.08", "dj_name": "T_GRAN | MILL"},
        {"week_day": "FRI.", "date": "11.08", 
                                        "dj_name": "HAYKAPRiCOTA | ARNIROCK"},
        {"week_day": "SAT.", "date": "12.08", "dj_name": "T_GRAN | DRRED"},
        {"week_day": "SUN.", "date": "13.08", "dj_name": "MILL | DRRED"},
    ]
    if request.method == "GET":
        return render_template('events_calendar.html', events=events)
    return redirect(url_for("cafe_plan"))

@app.route('/cafe_plan', methods=["GET", "POST"])
def cafe_plan():
    if request.method == "GET":
        return render_template('cafe_plan.html', tables=tables)
    return render_template("booking_table.html")

@app.route('/booking_table/<int:table_id>', methods=['POST'])
def booking_table(table_id):
    table = next((table for table in tables if table.id == table_id), None)
    
    if table and not table.booked:
        table.booked = True
        return redirect(url_for('booking_success', table_id=table_id))
    else:
        return "Table is not available for booking."
    
@app.route('/booking_success', methods=['GET', 'POST'])
def booking_success():
    if request.method == 'GET':  
        return render_template("booking_table.html")
    
    booking_handler = BookingControler()

    date = request.form['date']
    time = request.form['time']
    guests = int(request.form['guests'])
    booked = request.form["booked"]
    
    if booking_handler.is_booking_duplicate(date, time):
        return "Booking for this date and time already exists.\
                Please choose another date or time."
    
    booking_handler.insert_booking(date, time, guests, booked)
    send_booking_confirmation_email(date, time, guests)
    
    return render_template(
                "booking_success.html", 
                date=date, time=time, guests=guests
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':   
        return render_template("register.html")
    
    user_hadnler = UserControler()

    name = request.form["name"]
    sur_name = request.form["surname"]
    mail_address = request.form["mail"]
    user_name = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password"]
    
    error_message = user_hadnler.validate_registration(
                                mail_address,  password, password2
    )
    
    if error_message:
        return render_template("register.html", error_message=error_message)
    
    try:
        hashed_password = user_hadnler.hash_password(password)

        user_hadnler.insert_user(
                name, sur_name, mail_address, user_name, hashed_password
        )
        
        return redirect(url_for("success"))
    
    except IntegrityError:
        return render_template(
            "register.html",
            error_message="Username alredy exists. Please replace your username"
        )
        

@app.route('/success')
def success():
    with get_db() as con:
        cursor = con.cursor()
        cursor.execute("SELECT name, surname, mail, username FROM USER")
    
    return render_template("success.html")


@app.route('/qr_info', methods=['GET'])
def qr_info():
    return render_template(
        'qr_info.html', 
        booking_info="Additional information about\
            the booking will be shown here."
    )


 