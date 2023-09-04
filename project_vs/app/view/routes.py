from flask import render_template, request, redirect, url_for

from app import app
from app.utils import send_booking_confirmation_email
from app.main import UserController, BookingController


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return  render_template('login.html')
    
    user_ctrl = UserController()

    user_name = request.form["username"]
    password = request.form["password"]

    user_data = user_ctrl.is_user_valid(user_name)
    
    if not user_data or not user_ctrl.check_password(password, user_data[0]):
        return render_template(
            'login.html',
            error_message="*Invalid username or password. Please try again.",
            username=user_name
        )
    
    return redirect(url_for("events_calendar"))


@app.route('/events_calendar', methods=["GET", "POST"])
def events_calendar():
    if request.method == "GET":
        booking_ctrl = BookingController()
        return render_template(
            'events_calendar.html', 
            events=booking_ctrl.insert_events()
        )
 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':   
        return render_template("register.html")
    
    user_ctrl = UserController()
    
    try:
        user_ctrl.insert_user(request.form)
        return render_template("success.html")

    except Exception as ex:
        return redirect(url_for(
                "register", 
                error_message=ex,
                name=request.form["name"], 
                surname=request.form["surname"], 
                mail=request.form["mail"], 
                username=request.form["username"]
        ))


@app.route('/qr_info', methods=['GET'])
def qr_info():
    return render_template(
        'qr_info.html', 
        booking_info="Information about the booking will be shown here."
    )


@app.route('/get_booking_data', methods=["GET", "POST"])
def get_booking_data():
    if request.method == 'POST': 
        booking_ctrl = BookingController()  
        
        booking_data = request.json
        date = booking_data.get('date')
        time = booking_data.get('time')
        guests = booking_data.get('guests')
        
        try:
            booking_ctrl.insert_booking(booking_data)
            response = {
                'success': True, 
                'date': date, 
                'time': time, 
                'guests': guests
            }
            send_booking_confirmation_email(booking_data)
        except ValueError as ex:
            response = {'success': False, 'message': str(ex)}
        
        return response
        
                   
