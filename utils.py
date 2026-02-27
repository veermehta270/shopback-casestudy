# utils.py
import os
from pathlib import Path
from PIL import Image, ImageOps
import datetime
import json
import gdown  
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_config import *

CUSTOMER_FILE = Path("customers.json")

# Load customers
def load_customers():
    if CUSTOMER_FILE.exists():
        with open(CUSTOMER_FILE, "r") as f:
            return json.load(f)
    return {}

# Save customers
def save_customers(customers):
    with open(CUSTOMER_FILE, "w") as f:
        json.dump(customers, f, indent=4)

# Create folder for customer
def create_customer_folder(brand_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"{brand_name}_{timestamp}"
    path = Path("assets") / folder_name
    path.mkdir(parents=True, exist_ok=True)
    return path

# Validate file format
def validate_file(file_path):
    allowed_formats = ['.png', '.jpg', '.jpeg']
    ext = os.path.splitext(file_path)[1].lower()
    return ext in allowed_formats

# Resize image
def resize_image(image_path, sizes, save_folder):
    from PIL import Image

    img = Image.open(image_path).convert("RGBA")

    resized_paths = []

    for size in sizes:
        resized = img.resize(size)

        output = save_folder / "resized_500x500.png"
        resized.save(output)

        resized_paths.append(output)

    return resized_paths

# Invert image
def invert_image(image_path, save_folder):
    from PIL import Image, ImageOps

    img = Image.open(image_path).convert("RGBA")

    resized = img.resize((500,500))

    inverted = ImageOps.invert(resized.convert("RGB"))
    output = save_folder / "inverted.png"
    inverted.save(output)

    return output

# Create info.txt
def create_info_file(save_folder, brand_name, email, original_file, resized_files, inverted_file):
    info_path = save_folder / "info.txt"
    with open(info_path, "w") as f:
        f.write(f"Brand Name: {brand_name}\n")
        f.write(f"Email: {email}\n")
        f.write(f"Original File: {original_file}\n")
        f.write(f"Resized Files: {', '.join([str(f) for f in resized_files])}\n")
        f.write(f"Inverted File: {inverted_file}\n")
        f.write(f"Upload Time: {datetime.datetime.now()}\n")
    return info_path



def extract_drive_file_id(drive_link):
    """
    Extract file ID from Google Drive link
    """
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", drive_link)
    if match:
        return match.group(1)

    # alternative format
    match = re.search(r"id=([a-zA-Z0-9_-]+)", drive_link)
    if match:
        return match.group(1)

    raise ValueError("Invalid Google Drive link")


def download_drive_file(drive_link, save_folder):
    """
    Download file from Google Drive into save_folder
    """
    file_id = extract_drive_file_id(drive_link)

    output_path = Path(save_folder) / "drive_download.png"

    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    gdown.download(url, str(output_path), quiet=False)

    return output_path
    

def send_completion_email(customer_email, brand_name):

    subject = f"{brand_name} is Live on ShopBack 🎉"

    html_body = f"""
    <html>
    <body style="font-family: Arial; background-color:#f5f6fa; padding:20px;">
        <div style="
            max-width:600px;
            margin:auto;
            background:white;
            padding:30px;
            border-radius:10px;
        ">

            <h2 style="color:#FF2D55;">ShopBack</h2>

            <h3>Your Brand Page is Ready 🚀</h3>

            <p>Hello,</p>

            <p>
            Your brand <b>{brand_name}</b> has been successfully processed
            and is now live on ShopBack.
            </p>

            <div style="
                background:#f1f2f6;
                padding:15px;
                border-radius:6px;
                margin:20px 0;
            ">
                ✅ Logos validated<br>
                ✅ Assets resized<br>
                ✅ Brand page published
            </div>

            <p>
            Thank you for partnering with ShopBack!
            </p>

            <hr>

            <p style="font-size:12px;color:gray;">
            This is an automated notification from ShopBack Operations.
            </p>

        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = customer_email
    msg["Subject"] = subject

    msg.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True

    except Exception as e:
        print("Email error:", e)
        return False