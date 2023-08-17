import qrcode
from PIL import Image
from io import BytesIO
from flask_mail import Message

from app import mail


def generate_qr_code(data: str) -> Image:
    """
    Generate qr code

    Parameters
    ----------
    data : str

    Returns
    -------
    Image

    """

    # Opens an existing ticket image 
    ticket_image = Image.open("app/static/tickets.jpg")

    url = "http://127.0.0.1:5000/qr_info" 
    data_with_url = f"{data}\n\nMore information: {url}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Adds data_with_url to the QR code
    qr.add_data(data_with_url)
    # Generates the QR code 
    qr.make(fit=True)

    qr_code_image = qr.make_image(fill_color="black", back_color="white")
    qr_code_image = qr_code_image.resize((250, 250))  

    # The position on the ticket image where the QR code will be pasted.
    overlay_position = (100, 250)  

    ticket_image.paste(qr_code_image, overlay_position, qr_code_image)


    return ticket_image

def send_booking_confirmation_email(date: str, time: str, guests: int):
        """
        Send booking confirmation email

        Parameters
        ----------
        date : str
        time : str
        guest : str

        """
        booking_details = f"Date: {date}\nTime: {time}\nGuests: {guests}"
        qr_code = generate_qr_code(booking_details)

        # Hold the binary data of the QR code image.
        qr_code_bytes = BytesIO()
        qr_code_bytes.seek(0)
        qr_code.save(qr_code_bytes, format="PNG")

        msg = Message(
            'Table Booking Confirmation', 
            sender='your_email@example.com', 
            recipients=["tikkhachatryan01@gmail.com"]
        )
        msg.body = f"Thank you for booking a table at Evn Cafe & Drink House."\
                f"\nAttached please find your E-tickets.\n"\
                f"Please show them at the entrance on your mobile screen.\n"\
                f"Date: {date}\nTime: {time}\nGuests: {guests}"

        #Attaches the QR code image as a PNG file to the email 
        msg.attach("qr_code.png", "image/png", qr_code_bytes.getvalue())

        mail.send(msg)
    
