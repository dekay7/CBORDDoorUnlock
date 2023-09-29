import os
import requests
from playwright.sync_api import sync_playwright
from emailNotification import send_email
import datetime
from dotenv import load_dotenv

# Loading variables
env = load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
sender = os.getenv("SENDER")
app_pass = os.getenv("APPPASS")
recipient = [f"{username}@hawk.iit.edu"]

# Url's and variables
login_url = "https://cardadmin.iit.edu/login/ldap.php"
open_door_url = "https://cardadmin.iit.edu/student/openmydoor.php"
headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}

# Initialize a session for requests
session = requests.Session()

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()

    # Initial get request to get __sesstok
    page.goto(login_url, wait_until='domcontentloaded')

    # Login using Playwright
    page.fill('input[name="user"]', username)
    page.fill('input[name="pass"]', password)
    page.click('input[type="submit"]')
    page.wait_for_load_state("load", timeout=120000)

    # Extract cookies from Playwright context and set them in the requests session
    cookies = page.context.cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Post request to open the door using the requests session
    payload = {
        'doorType': '1',
        'answeredYes': 'yes',
        '__sesstok': page.evaluate("() => window.__sesstok")
    }
    open_door_response = session.post(open_door_url, headers=headers, data=payload)

    browser.close()

# Send email notification
if sender and sender != "senderemail@gmail.com":
    time = datetime.datetime.now()
    try:
        send_email(subject=f"Door Unlocked @ {time}", body=f"Your door was unlocked @ {time}.", sender=sender, recipients=recipient, password=app_pass)
    except Exception as e:
        raise Exception("Error sending email:", str(e))