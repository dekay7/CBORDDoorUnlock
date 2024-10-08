from playwright.sync_api import sync_playwright

# Url's and variables
login_url = "https://cardadmin.iit.edu/login/ldap.php"
open_door_url = "https://cardadmin.iit.edu/student/openmydoor.php"
cookies = [
    {"name": "PHPSESSID", "value": "php_sess_id", "url": "https://cardadmin.iit.edu"},
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
    context.add_cookies(cookies)
    page = context.new_page()
    page.goto(open_door_url, wait_until='load')
    page.click('input[type="submit"]')
    browser.close()