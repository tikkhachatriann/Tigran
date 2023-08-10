import qrcode

def generate_qr_code(data):
    url = "http://127.0.0.1:5000/qr_info" 
    data_with_url = f"{data}\n\nMore information: {url}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_with_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img