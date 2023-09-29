import os
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

with sync_playwright() as p:
    # Create new playwright browser and act like a mobile user-agent
    browser = p.chromium.launch()
    context = browser.new_context(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
    page = context.new_page()
    
    # Visit login page
    page.goto(login_url, wait_until='domcontentloaded')

    # Login using Playwright
    page.fill('input[name="user"]', username)
    page.fill('input[name="pass"]', password)
    page.click('input[type="submit"]')
    page.wait_for_load_state("load", timeout=None)
    page.goto(open_door_url, wait_until='domcontentloaded')
    page.click('input[type="submit"]')
    browser.close()

# Send email notification
if sender and sender != "senderemail@gmail.com":
    time = datetime.datetime.now()
    try:
        send_email(subject=f"Door Unlocked @ {time}", body=f"Your door was unlocked @ {time}.", sender=sender, recipients=recipient, password=app_pass)
    except Exception as e:
        raise Exception("Error sending email:", str(e))