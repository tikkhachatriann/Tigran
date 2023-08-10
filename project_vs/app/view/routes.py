from app import app, mail
from app.database import get_cursor, get_db
from app.models.qr_code import generate_qr_code
from flask import render_template, request
from flask_mail import Message
from sqlite3 import IntegrityError
from io import BytesIO
import bcrypt


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/events_calendar')
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
    return render_template('events_calendar.html', events=events)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form["usrnm"]
        password = request.form["psw"]

        cursor = get_cursor()
        cursor.execute(
            "SELECT password FROM USER WHERE username = ?", (user_name,)
        )
        
        result = cursor.fetchone()

        if result:
            hashed_password_from_db = result[0]

            if bcrypt.checkpw(password.encode('utf-8'),hashed_password_from_db):
                return render_template("booking_table.html")
            else:
                return "Invalid username or password. Please try again."
       
        else: 
            return "User not found. Please check your username."
    
    return  render_template('login.html')


@app.route('/success')
def success():
    with get_db() as con:
        cursor = con.cursor()
        cursor.execute("SELECT name, surname, mail, username FROM USER")
    
    return render_template("success.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form["name"]
        sur_name = request.form["surnm"]
        mail_address = request.form["mail"]
        user_name = request.form["usrnm"]
        password = request.form["psw"]
        password2 = request.form["psw2"]
        
        if password == password2:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                            bcrypt.gensalt())
            try:
                with get_db() as con:
                    cursor = con.cursor()
                    cursor.execute(
                        "INSERT INTO USER( \
                            name, surname, mail, username, password \
                        )  \
                        VALUES(?, ?, ?, ?, ?)", (  
                            name, sur_name, mail_address, 
                            user_name, hashed_password
                        )
                    )
                return render_template("success.html")
            
            except IntegrityError:
                return "Username alredy exists. Please replace your username"
        
        else:
            return "The passwords do not match. Please try again."
        
    return render_template("register.html")


@app.route('/booking_table', methods=['GET', 'POST'])
def booking_table():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
       
        return render_template('booking_success.html', date=date, time=time)
    return render_template('booking_table.html')


@app.route('/booking_success', methods=['GET', 'POST'])
def booking_success():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        guests = int(request.form['guests'])
        booked = bool(request.form["booked"])
        
        with get_db() as con:
            cursor = con.cursor()
            cursor.execute("SELECT id FROM BOOKING_TABLE  \
                           WHERE date = ? AND time = ?", (date, time))

            existing_booking = cursor.fetchone()

        if  existing_booking:
            return "Booking for this date and time already exists.\
                    Please choose another date or time."
        else:
            cursor.execute(
                    "INSERT INTO BOOKING_TABLE( \
                    date, time, count, booked) VALUES(?, ?, ?, ?)",
                    (date, time, guests, booked)
            )
            con.commit()
            
            booking_details = f"Date: {date}\nTime: {time}\nGuests: {guests}"
                        
            qr_code = generate_qr_code(booking_details)

            qr_code_bytes = BytesIO()
            qr_code_bytes.seek(0)
            qr_code.save(qr_code_bytes, format="PNG")
            
            msg = Message(
                        'Table Booking Confirmation', 
                        sender='your_email@example.com', 
                        recipients=["tikhachatryan01@gmail.com"]
            )
            msg.body = f'Thank you for booking a table at Evn Cafe & Drink House\
                        Attached please find your E-tickets.\
                        Please show them at the entrance on your mobile screen \
                        Date: {date}\nTime: {time}\nGuests: {guests} '
        
            msg.attach("qr_code.png", "image/png", qr_code_bytes.getvalue())
            mail.send(msg)

            return render_template(
                                "booking_success.html", 
                                date=date, time=time, guests=guests
            )
    return render_template("booking_table.html")
        

@app.route('/qr_info', methods=['GET'])
def qr_info():
    
    booking_info = "Additional information about the booking will be shown here."
    return render_template('qr_info.html', booking_info=booking_info)


 