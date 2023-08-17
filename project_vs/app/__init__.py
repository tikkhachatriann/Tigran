from flask import Flask
from flask_mail import Mail


app = Flask(__name__)

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





