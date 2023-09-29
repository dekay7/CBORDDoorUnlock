# Import modules
from requests_html import HTMLSession
from bs4 import BeautifulSoup

# Url's and variables
login_url = "https://cardadmin.iit.edu/login/ldap.php"
menu_url = "https://cardadmin.iit.edu/m_menu.php"
open_door_url = "https://cardadmin.iit.edu/student/openmydoor.php"
headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}
cookies = {
    "PHPSESSID": "php_sess_id",
    "CsgUserData": "csg_user_data",
}

# Creating a requests session to store and pass cookies
with HTMLSession() as s:
    # Get menu page
    menu = s.get(menu_url, headers=headers, cookies=cookies)
    menu.html.render(timeout=120)
    soup = BeautifulSoup(menu.content, 'html.parser')
    # Menu session token
    session_token_script = soup.find('script', language="Javascript").text
    session_token = session_token_script.split("__sesstok = '")[1].split("';")[0]
    print(session_token)

    # Post request to open the door
    payload = {
        'doorType': '1',
        'answeredYes': 'yes',
        '__sesstok': session_token
    }
    open_door = s.post(open_door_url, headers=headers, data=payload, cookies=cookies)
    open_door.html.render(timeout=120)
    soup = BeautifulSoup(open_door.content, 'html.parser')
    # Opened door session token
    session_token_script = soup.find('script', language="Javascript").text
    session_token = session_token_script.split("__sesstok = '")[1].split("';")[0]
    print(session_token)