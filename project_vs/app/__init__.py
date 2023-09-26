import os
from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager

from app.user import User


app = Flask(__name__)

app.secret_key = os.urandom(24)
login_manager = LoginManager(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user_data = User.get(user_id)
    if user_data:
        return User(user_data.id)
    

# Configuration dictionary
app.config.update(
    MAIL_SERVER="smtp.Gmail.com",
    MAIL_PORT=587, 
    MAIL_USE_TLS=True,
    MAIL_USERNAME="tigran.khachatryan@vxsoft.com",
    MAIL_PASSWORD="asoktlidfgunnbki"
)

# Initialize Flask-Mail
mail = Mail(app)
    
# Import routes after initializing the app and mail    
from app.view import routes





