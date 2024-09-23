from flask import Flask
from openDoor import DoorModule

app = Flask(__name__)
door_module = DoorModule()
print("Created door module object")

@app.route('/open_sesame', methods=['GET'])
def open_sesame():
    conditions = ""
    if door_module.browser is None:
        conditions = conditions + "Browser instance non-existant. "
        if not door_module.initialize_browser():
            return "Could not initialize browser. " + conditions
        if not door_module.login():
            return "Failed to log in. " + conditions
    else:
        print("Browser exists")
        if not door_module.is_logged_in():
            conditions = conditions + "Browser instance not authenticated. "
            print("Not authenticated")
            if not door_module.login():
                return "Failed to log in. " + conditions
        else:
            conditions = conditions + "Browser instance authenticated. "
            print("Already authenticated")
    if not door_module.open_door():
        return "Failed to open door. " + conditions
    if door_module.send_email():
        conditions = conditions + "Sent email. "
    return "Door unlocked. " + conditions

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=False)