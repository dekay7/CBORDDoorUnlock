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
        print(door_module.initialize_browser())
        print(door_module.login())
    else:
        conditions = conditions + "Browser instance exists. "
        print("Browser exists")
        if not door_module.is_logged_in():
            conditions = conditions + "Browser instance not authenticated. "
            print("Not authenticated")
            print(door_module.login())
        else:
            conditions = conditions + "Browser instance authenticated. "
            print("Already authenticated")
    print(door_module.open_door())
    print(door_module.send_email())
    return "Door unlocked. Conditions: " + conditions

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=False)