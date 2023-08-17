from flask import Flask
from flask_mail import Mail

app = Flask(__name__)


app.config.update(
            MAIL_SERVER="smtp.Gmail.com",
            MAIL_PORT=587, 
            MAIL_USE_TLS=True,
            MAIL_USERNAME="tigran.khachatryan@vxsoft.com",
            MAIL_PASSWORD="asoktlidfgunnbki"
)

mail = Mail(app)
    
from app.view import routes





