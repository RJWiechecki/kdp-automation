# KDP Automation

This project automates the daily download and email delivery of Kindle Direct Publishing (KDP) dashboard reports.

## 🔄 Project Workflow

1. **Open KDP Dashboard** using a trusted Firefox profile
2. **Inject valid cookies** if available
3. **Navigate to Reports page** and **download** the latest sales report
4. **Email** the downloaded file as an attachment to the configured recipient
5. **Automated** by Linux/macOS `crontab`

---

## 🔹 Requirements

- Python 3.8+
- Firefox browser installed
- `geckodriver` installed (and available in your PATH)
- Google account with an **App Password** generated (for email sending)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔹 Setup Instructions

### 1. Clone the repository

```bash
cd ~/Dev/
git clone https://github.com/rjwiechecki/kdp-automation.git
cd kdp-automation
```

### 2. Create `.env` file

Create a `.env` file in the project root:

```bash
touch .env
```

Add the following environment variables:

```bash
GMAIL_SENDER=your.email@gmail.com
GMAIL_RECEIVER=recipient.email@gmail.com
GMAIL_PASSWORD=your-app-specific-password
```

### 3. Set up Firefox Profile

- Create a **dedicated Firefox profile** called `FirefoxUserDataClean` under `browser_profiles/`
- Import bookmarks, cookies, and extensions manually
- Log into Amazon & KDP and disable OTP on trusted browser if possible

To manually launch and configure it:

```bash
/Applications/Firefox.app/Contents/MacOS/firefox --no-remote -profile /path/to/browser_profiles/FirefoxUserDataClean
```

### 4. Manual Cookie Capture (Optional First Run)

If cookies aren't captured automatically:

```bash
python3 cookie_imports.py
```

Follow prompts to login manually and capture cookies.

### 5. Test the Scraper

```bash
python3 kdp_report_scraper.py
```

### 6. Test the Email Sender

```bash
python3 send_email_report.py
```

### 7. Set up Cron Jobs (Automation)

Edit your `crontab`:

```bash
crontab -e
```

Example (run at 6:01 AM daily):

```bash
# Step 1: Download KDP Report
1 6 * * * /usr/bin/python3 /path/to/kdp_report_scraper.py

# Step 2: Send KDP Report via Email
6 6 * * * /usr/bin/python3 /path/to/send_email_report.py
```

---

## 🌐 Project Structure

```
.kdp-automation/
├── browser_profiles/
│   └── FirefoxUserDataClean/
├── cookies.pkl
├── .env
├── kdp_report_scraper.py
├── send_email_report.py
├── README.md
```

---

## 🏆 License

MIT License

Copyright (c) 2025 RJ Wiechecki

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


