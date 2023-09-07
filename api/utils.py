import qrcode
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

def generate_qr_code_data(qr_data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the image to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')

    # Create an InMemoryUploadedFile from the image bytes
    qr_code = InMemoryUploadedFile(
        img_bytes,
        None,
        f'invoice_qr_code.png',
        'image/png',
        img_bytes.tell(),
        None
    )

    return qr_code
