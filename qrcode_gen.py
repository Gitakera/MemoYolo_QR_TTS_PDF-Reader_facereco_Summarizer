import qrcode

def generate_qr_code(text, box_size=10, border=4, fill_color="black", back_color="white", logo=None):
    """Generate a QR code from the given text with customization options."""
    qr = qrcode.QRCode(version=1, box_size=box_size, border=border)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

    if logo:
        logo = logo.resize((img.size[0] // 4, img.size[1] // 4))
        pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        img.paste(logo, pos)

    return img

