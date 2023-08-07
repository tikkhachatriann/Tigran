from app import app, mail
from app.database import get_cursor, get_db
from flask import render_template, request
from flask_mail import Message
from sqlite3 import IntegrityError
import bcrypt


@app.route('/')
def home():
    return render_template('home.html')


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

        if result is not None:
            hashed_password_from_db = result[0]

            if bcrypt.checkpw(password.encode('utf-8'),hashed_password_from_db):
                return render_template("booking_table.html")
            else:
                return "Invalid username or password. Please try again."
       
        else:
            return "User not found. Please check your username."
    
    return  render_template('login.html')

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
       
        msg = Message(
                    'Table Booking Confirmation', 
                    sender='your_email@example.com', 
                    recipients=["tikhachatryan01@gmail.com"]
        )
        msg.body = f'Thank you for booking a table at Evn Cafe & Drink House.\
                    \n\nDate: {date}\nTime: {time}\nGuests: {guests}'
        mail.send(msg)

        return render_template(
                              "booking_success.html", 
                               date=date, time=time, guests=guests
                )
    

@app.route('/success')
def success():
    with get_db() as con:
        cursor = con.cursor()
        cursor.execute("SELECT name, surname, mail, username FROM USER")
    
    return render_template("success.html")

