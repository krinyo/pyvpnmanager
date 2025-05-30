import qrcode
import os

def generate_qr_code(vless_string, user_id):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(vless_string)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    qr_path = f"qr_{user_id}.png"
    img.save(qr_path)
    return qr_path