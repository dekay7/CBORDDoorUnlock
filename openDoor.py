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
    
    # Get session token
    page.goto(login_url, wait_until='domcontentloaded', timeout=None)
    content = page.content()
    session_token_start = content.find("__sesstok = '") + len("__sesstok = '")
    session_token_end = content.find("';", session_token_start)
    session_token = content[session_token_start:session_token_end]

    # Login using post request
    payload = {
        'user': username,
        'pass': password,
        '__sesstok': session_token,
    }
    response = context.request.post(login_url, data=payload, timeout=None)
    page.goto(open_door_url, wait_until='domcontentloaded', timeout=None)
    content = page.content()
    session_token_start = content.find("__sesstok = '") + len("__sesstok = '")
    session_token_end = content.find("';", session_token_start)
    session_token = content[session_token_start:session_token_end]

    # Open door using post request
    payload = {
        'doorType': 1,
        'answeredYes': "yes",
        '__sesstok': session_token
    }
    response = context.request.post(open_door_url, data=payload, timeout=None)

    # End browser session
    browser.close()

# Send email notification
if sender and sender != "senderemail@gmail.com":
    time = datetime.datetime.now()
    try:
        send_email(subject=f"Door Unlocked @ {time}", body=f"Your door was unlocked @ {time}.", sender=sender, recipients=recipient, password=app_pass)
    except Exception as e:
        raise Exception("Error sending email:", str(e))