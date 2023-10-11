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
        self.login_url = "https://cardadmin.iit.edu/login/ldap.php"
        self.open_door_url = "https://cardadmin.iit.edu/student/openmydoor.php"
        self.env = load_dotenv()
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
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
        return("Browser initialized")

    def is_logged_in(self):
        # Check if browser is logged in to CBORD
        self.page.goto(self.open_door_url, wait_until='domcontentloaded', timeout=0)
        self.content = self.page.content()
        if "<h2>Login</h2>" in self.content:
            return False
        return True

    def login(self):
        # Get initial session token to pass to login
        print("Getting session token")
        self.page.goto(self.login_url, wait_until='domcontentloaded', timeout=0)
        self.content = self.page.content()
        self.session_token_start = self.content.find("__sesstok = '") + len("__sesstok = '")
        self.session_token_end = self.content.find("';", self.session_token_start)
        self.session_token = self.content[self.session_token_start:self.session_token_end]
        print(f"Pre-login session token: {self.session_token}")
        # Login using the payload
        self.payload = {
            'user': self.username,
            'pass': self.password,
            '__sesstok': self.session_token,
        }
        print("Logging in")
        self.context.request.post(self.login_url, data=self.payload, timeout=0)
        # Verify login and get authenticated session token
        self.page.goto(self.open_door_url, wait_until='load', timeout=0)
        print("Logged in")
        print("Getting session token")
        self.content = self.page.content()
        self.session_token_start = self.content.find("__sesstok = '") + len("__sesstok = '")
        self.session_token_end = self.content.find("';", self.session_token_start)
        self.session_token = self.content[self.session_token_start:self.session_token_end]
        print(f"Post-login session token: {self.session_token}")
        return "Login confirmed"

    def open_door(self):
        # Open the door using the payload
        print("Opening door")
        self.payload = {
            'doorType': 1,
            'answeredYes': "yes",
            '__sesstok': self.session_token
        }
        self.context.request.post(self.open_door_url, data=self.payload, timeout=0)
        return("Opened door")

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
                return("Email sent")
            except Exception as e:
                raise Exception("Error sending email:", str(e))

    def close_browser(self):
        # CLose the browser (not implemented in Flask server)
        self.browser.close()
        print("Closed browser")
        self.playwright.stop()
        print("Stopped playwright")