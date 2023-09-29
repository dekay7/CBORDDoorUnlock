# Import modules
import os
from requests_html import HTMLSession
from emailNotification import send_email
import datetime
from bs4 import BeautifulSoup
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

# Creating a requests session to store and pass cookies
with HTMLSession() as s:
    # Initial get request to get __sesstok
    visit = s.get(login_url, headers=headers)
    visit.html.render(timeout=120)
    soup = BeautifulSoup(visit.content, 'html.parser')
    # First session token
    session_token_script = soup.find('script', language="Javascript").text
    session_token = session_token_script.split("__sesstok = '")[1].split("';")[0]
    print(session_token)

    # Post request to login to cardadmin
    payload = {
        'user': username,
        'pass': password,
        '__sesstok': session_token,
    }
    login = s.post(login_url, headers=headers, data=payload)
    login.html.render(timeout=120)
    soup = BeautifulSoup(login.content, 'html.parser')
    # Logged in session token
    session_token_script = soup.find('script', language="Javascript").text
    session_token = session_token_script.split("__sesstok = '")[1].split("';")[0]
    print(session_token)

    # Post request to open the door
    payload = {
        'doorType': '1',
        'answeredYes': 'yes',
        '__sesstok': session_token
    }
    open_door = s.post(open_door_url, headers=headers, data=payload)
    open_door.html.render(timeout=120)
    soup = BeautifulSoup(open_door.content, 'html.parser')
    # Opened door session token
    session_token_script = soup.find('script', language="Javascript").text
    session_token = session_token_script.split("__sesstok = '")[1].split("';")[0]
    print(session_token)

# Send email notification
if sender != "senderemail@gmail.com" or sender != None:
    time = datetime.datetime.now()
    try:
        send_email(subject=f"Door Unlocked @ {time}", body=f"Your door was unlocked @ {time}.", sender=sender, recipients=recipient, password=app_pass)
    except:
        raise Exception("Error sending email")