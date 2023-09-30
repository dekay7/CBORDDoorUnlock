from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/open_sesame', methods=['GET'])
def open_sesame():
    try:
        subprocess.run(['/root/open_door/venv/bin/python3', '/root/open_door/openDoor.py'], check=True, capture_output=True)
        return "Door unlocked."
    except subprocess.CalledProcessError as e:
        return f"Error: {str(e)}\nSTDOUT: {e.stdout.decode()}\nSTDERR: {e.stderr.decode()}", 500
    except Exception as e:
        return f"Unexpected Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)