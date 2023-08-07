from flask import Flask
from flask_mail import Mail

app = Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.Gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "tigran.khachatryan@vxsoft.com"
app.config["MAIL_PASSWORD"] = "asoktlidfgunnbki"
mail = Mail(app)

from app.view import routes





