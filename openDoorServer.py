from flask import Flask
from openDoorBeta import DoorModule

app = Flask(__name__)
door_module = DoorModule()
print("Created door module object")

@app.route('/open_sesame', methods=['GET'])
def open_sesame():
    if door_module.browser is None:
        print(door_module.initialize_browser())
        print(door_module.login())
    else:
        print("Browser exists")
        if not door_module.is_logged_in():
            print("Not logged in")
            print(door_module.login())
        else:
            print("Already logged in")
    print(door_module.open_door())
    print(door_module.send_email())
    return "Door unlocked."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)