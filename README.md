# ShopBack Brand Automation

A lightweight internal tool for automating brand logo onboarding — from upload to approval to publishing — built with Streamlit.

---

## Overview

This tool replaces a manual brand asset workflow with a structured 4-step pipeline:

```
Upload → Auto-Process → Human Approval → Finalize & Notify
```

An ops team member uploads a brand's logo. The system automatically generates the required asset variants, queues it for review, and sends a confirmation email to the brand once approved.

---

## Project Structure

```
shopback-brand-automation/
│
├── main.py            # UI layer — all 4 pages rendered here
├── utils.py           # Logic layer — image processing, file I/O, email
├── email_config.py    # SMTP credentials (EMAIL_ADDRESS, EMAIL_PASSWORD, etc.)
├── customers.json     # Auto-generated — persists all customer records
│
└── assets/            # Auto-generated — one folder per brand submission
    └── BrandName_20250101_120000/
        ├── original.png
        ├── resized_500x500.png
        ├── inverted.png
        └── info.txt
```

---

## Pages

### 1. Customer Registration / Upload
Create a new brand record or update an existing one. Upload 1–3 logos (PNG/JPG) or provide a Google Drive link. On submission, the app:
- Saves the original logo
- Generates a **500×500 resized** version
- Generates a **colour-inverted** version
- Writes the brand to `customers.json` with status `Pending`

### 2. Pending Approvals
Lists all brands with `Pending` status. An internal reviewer previews the processed images and clicks **Finalize** to:
- Update status to `Finalized` in `customers.json`
- Trigger a confirmation email to the brand

### 3. Dashboard
Read-only gallery of all `Finalized` brands, showing the three asset variants (original, resized, inverted) side by side.

### 4. Operations Analytics
- Pie chart showing distribution of brand statuses (Pending vs Finalized)
- Per-brand progress bar tracking position in the workflow across 4 stages: Uploaded → Processed → Pending → Finalized

---

## How Data is Stored

There is no database. All state lives in `customers.json`:

```json
{
  "Nike": {
    "email": "partner@nike.com",
    "folder": "assets/Nike_20250101_120000",
    "status": "Pending"
  }
}
```

This file is read on every page load and written on every state change (submission or finalization).

---

## Image Processing Pipeline (`utils.py`)

| Function | Input | Output |
|---|---|---|
| `validate_file()` | File path | `True` if PNG/JPG |
| `resize_image()` | Original + sizes | `resized_500x500.png` |
| `invert_image()` | Original | `inverted.png` (also resized to 500×500) |
| `create_info_file()` | Brand metadata | `info.txt` in brand folder |

---

## Email Notifications

On finalization, `send_completion_email()` sends an HTML email to the brand contact via SMTP. Credentials are pulled from `email_config.py`.

```python
# email_config.py (you must create this)
EMAIL_ADDRESS = "your@email.com"
EMAIL_PASSWORD = "your_app_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

> ⚠️ Never commit `email_config.py` to version control. Add it to `.gitignore`.

---

## Setup & Installation

**1. Clone the repo and install dependencies**

```bash
pip install streamlit pillow gdown
```

**2. Create `email_config.py`** with your SMTP credentials (see above).

**3. Run the app**

```bash
streamlit run main.py
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `Pillow` | Image resizing and inversion |
| `gdown` | Google Drive file downloads |
| `smtplib` | Email sending (stdlib) |
