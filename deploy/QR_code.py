import qrcode

# URL of your Heroku app
url = "https://mdamainpage-26dd5ba1b110.herokuapp.com"

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill_color="black", back_color="white")

# Save the image
img.save("pages/assets/heroku_app_qr.png")

print("QR code generated and saved as heroku_app_qr.png")
