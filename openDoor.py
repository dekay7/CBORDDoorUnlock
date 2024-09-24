# OS Modules
import os
from dotenv import load_dotenv
# Email Modules
import datetime
import smtplib
from email.mime.text import MIMEText
# Operational Modules
from playwright.sync_api import sync_playwright

class DoorModule:
    def __init__(self):
        # Setting variables when initialized
        self.env = load_dotenv()
        self.login_url = os.getenv("LOGINURL")
        self.open_door_url = os.getenv("DOORURL")
        self.username = os.getenv("LOGINUSER")
        self.password = os.getenv("PASS")
        self.sender = os.getenv("SENDER")
        self.app_pass = os.getenv("APPPASS")
        self.browser = None
        self.page = None
        self.context_manager = sync_playwright()

    def initialize_browser(self):
        # Initialize playwright browser
        print("Initializing browser")
        self.playwright = self.context_manager.start()
        self.browser = self.playwright.chromium.launch()
        self.context = self.browser.new_context(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
        self.page = self.context.new_page()
        return True

    def is_logged_in(self):
        # Check if browser is logged in to CBORD
        self.page.goto(self.open_door_url, wait_until='load', timeout=0)
        self.content = self.page.content()
        if "<h2>Login</h2>" in self.content:
            return False
        return True

    def login(self):
        # Get initial session token to pass to login
        print("Getting unauthenticated session token")
        self.page.goto(self.login_url, wait_until='load', timeout=0)
        cookies = self.page.context.cookies()
        for cookie in cookies:
            if cookie['name'] == 'PHPSESSID':
                self.unauth_token = cookie['value']
                break
        else:
            raise Exception("PHPSESSID cookie not found.")
        print(f"Unauthenticated session token: {self.unauth_token}")
        # Login using the payload
        print(f"Logging in with {self.username} and {self.password}")
        self.page.type('input[name="user"]', self.username)
        self.page.type('input[name="pass"]', self.password)
        self.page.click('input[type="submit"]', timeout=0)
        # Verify login and get authenticated session token
        self.page.goto(self.open_door_url, wait_until='load', timeout=0)
        print("Getting authenticated session token")
        cookies = self.page.context.cookies()
        for cookie in cookies:
            if cookie['name'] == 'PHPSESSID':
                self.auth_token = cookie['value']
                break
        else:
            raise Exception("PHPSESSID cookie not found.")
        if self.unauth_token != self.auth_token:
            print(f"Authenticated session token: {self.auth_token}")
            return True
        else:
            return False

    def open_door(self):
        # Open the door using the payload
        print("Opening door")
        self.page.click('input[type="submit"]')
        self.page.wait_for_load_state(state="load", timeout=0)
        if "Approved" in self.page.content():
            return True
        else:
            return False

    def send_email(self):
        # Send email notification
        if self.sender != "senderemail@gmail.com" or None:
            self.time = datetime.datetime.now()
            self.recipient = f"{self.username}@hawk.iit.edu"
            try:
                msg = MIMEText(f"Your door was unlocked @ {self.time}.")
                msg['Subject'] = f"Door Unlocked @ {self.time}"
                msg['From'] = self.sender
                msg['To'] = ', '.join(self.recipient)
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                    smtp_server.login(self.sender, self.app_pass)
                    smtp_server.sendmail(self.sender, self.recipient, msg.as_string())
                return True
            except Exception as e:
                raise Exception("Error sending email:", str(e))
        else:
            return False

    def close_browser(self):
        # CLose the browser (not implemented in Flask server)
        self.browser.close()
        print("Closed browser")
        self.playwright.stop()
        print("Stopped playwright")
