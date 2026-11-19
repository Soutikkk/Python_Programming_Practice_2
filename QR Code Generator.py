
import qrcode
from pathlib import Path
from datetime import datetime


OUTPUT_DIR = Path("Generated_QR_Codes")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_qr(data, filename, fill="black", back="white"):
    """Generate and save a QR code."""

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4
    )

    qr.add_data(data)
    qr.make(fit=True)

    image = qr.make_image(
        fill_color=fill,
        back_color=back
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filepath = OUTPUT_DIR / f"{filename}_{timestamp}.png"

    image.save(filepath)

    print("\nQR Code generated successfully!")
    print(f"Saved at: {filepath.resolve()}")


def text_qr():
    """Generate QR code for text or URL."""

    data = input("\nEnter text or website URL: ").strip()

    if not data:
        print("Input cannot be empty!")
        return

    generate_qr(data, "Text_QR")


def wifi_qr():
    """Generate Wi-Fi connection QR code."""

    ssid = input("\nEnter Wi-Fi name: ")
    password = input("Enter Wi-Fi password: ")

    security = input(
        "Security type (WPA/WEP/nopass) [WPA]: "
    ).strip().upper() or "WPA"

    if security not in ("WPA", "WEP", "NOPASS"):
        print("Invalid security type!")
        return

    if security == "NOPASS":
        security = "nopass"
        password = ""

    def escape_wifi(value):
        for char in ("\\", ";", ",", ":", '"'):
            value = value.replace(char, "\\" + char)
        return value

    data = (
        f"WIFI:T:{security};"
        f"S:{escape_wifi(ssid)};"
        f"P:{escape_wifi(password)};;"
    )

    generate_qr(data, "WiFi_QR")


def contact_qr():
    """Generate contact QR code using vCard."""

    name = input("\nEnter full name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()

    def safe_vcard(value):
        return (
            value.replace("\\", "\\\\")
                 .replace("\n", "\\n")
                 .replace(",", "\\,")
                 .replace(";", "\\;")
        )

    data = (
        "BEGIN:VCARD\n"
        "VERSION:3.0\n"
        f"FN:{safe_vcard(name)}\n"
        f"TEL:{safe_vcard(phone)}\n"
        f"EMAIL:{safe_vcard(email)}\n"
        "END:VCARD"
    )

    generate_qr(data, "Contact_QR")


def custom_qr():
    """Generate QR code with custom colors."""

    data = input("\nEnter text or URL: ").strip()

    if not data:
        print("Input cannot be empty!")
        return

    fill = input(
        "Enter QR color (default black): "
    ).strip() or "black"

    back = input(
        "Enter background color (default white): "
    ).strip() or "white"

    try:
        generate_qr(data, "Custom_QR", fill, back)
    except (ValueError, TypeError) as error:
        print(f"Invalid color: {error}")


def main():
    while True:
        print("\n" + "=" * 45)
        print("           QR CODE GENERATOR")
        print("=" * 45)

        print("1. Generate Text / URL QR Code")
        print("2. Generate Wi-Fi QR Code")
        print("3. Generate Contact QR Code")
        print("4. Generate Custom Color QR Code")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            text_qr()

        elif choice == "2":
            wifi_qr()

        elif choice == "3":
            contact_qr()

        elif choice == "4":
            custom_qr()

        elif choice == "5":
            print("\nThank you for using QR Code Generator!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
