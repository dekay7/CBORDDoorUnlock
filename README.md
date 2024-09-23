# CBORD MobileID/CardAdmin Door Opener
Due to this program's reliance on [Playwright](https://playwright.dev/python/), it is only compatible with Debian/Ubuntu, macOS, and Windows.

## ⚠️DISCLAIMER:
Any malicious use of this program is not the responsibility of the author. By downloading and using this program, you agree that you, and any other parties involved in your implementation of this program, are entirely responsible for its use/misuse. <br>

Please do not do stupid shit. The goal of this program is to provide an alternate method of room access as a quality of life improvement. No malicious intent exists behind the development of this program. 

## Automatic Installation (Debian/Ubuntu, macOS):
**This will perform a wholistic install that has been thoroughly tested on Alpine Linux.** <br>

Install dependencies and run the `install.sh` script:
```bash
apt update && apt install -y sudo curl && curl -sSL https://raw.githubusercontent.com/dekay7/CBORDDoorUnlock/main/install.sh | bash
```

## Docker Installation (Linux, macOS, Windows):
Make sure you have Docker already installed on your device (that will be acting as the server). <br>

Download `CBORDDoorUnlock_Docker.zip` from the [latest release](https://github.com/dekay7/CBORDDoorUnlock/releases/latest). Using `nano`, `vim`, or any other text editor, assign the following variables in `Dockerfile` to the appropriate values:
- For `ENV LOGINUSER=`, replace "oktausername1" with your OKTA username
- For `ENV PASS=`, replace "okta_p@ssword" with your OKTA password
Open a terminal in the same directory as the `Dockerfile` and build a Docker image using the following command:
```bash
docker build -t open_door .
```
Run a Docker container with host port 5000 using the following command:
```bash
docker run -p 5000:5000 --restart always open_door
```

#### Optional:
If you would like to receive emails every time your door is unlocked, assign the following variables in `Dockerfile` to the appropriate values: 
- For `ENV SENDER=`, replace "senderemail@gmail.com" with a sender Gmail to receive door unlock notifications from
- For `ENV APPPASS=`, replace "aaaa bbbb cccc dddd" with:
    - Your Gmail password **(if you <u>ARE NOT</u> using 2FA)**
    - A generated app password **(if you <u>ARE</u> using 2FA)**

## Manual Installation:
Rename `example.env` to `.env` using the following command:
```bash
sudo mv example.env .env
```
Using `nano`, `vim`, or any other text editor, assign the following variables in `.env` to the appropriate values:
- For `LOGINUSER=`, replace "oktausername1" with your OKTA username
- For `PASS=`, replace "okta_p@ssword" with your OKTA password

#### Optional:
If you would like receive emails every time your door is unlocked, assign the following variables in `.env` to the appropriate values:
- For `SENDER=`, replace "senderemail@gmail.com" with a sender Gmail to receive door unlock notifications from
- For `APPPASS=`, replace "aaaa bbbb cccc dddd" with:
    - Your Gmail password **(if you <u>ARE NOT</u> using 2FA)**
    - A generated app password **(if you <u>ARE</u> using 2FA)**

#### Manual Service Configuration:
Using `nano`, `vim`, or any other text editor, edit "/root/open_door/openDoorServer.py" in `openDoor.service` to the file path of `openDoorServer.py`. 

Move `openDoor.service` to /etc/systemd/system using the following command:
```bash
sudo mv openDoor.service /etc/systemd/system
```
Allow `openDoor.service` to run on startup using the following command:
```bash
sudo systemctl enable openDoor.service
```
Start `openDoor.service` using the following command:
```bash
sudo systemctl start openDoor.service
```
Check whether `openDoor.service` is running using the following command:
```bash
sudo systemctl status openDoor.service
``` 

## Opening Your Door:
### If using `openDoor.py`:
After configuring the `.env` file, to use the python script, simply run it.

### If using `openDoor.service`:
After configuration and service configuration, as long as `openDoor.service` is enabled and running, you may visit the local IP of the host server, followed by the port, and the subdirectory. <br>
For example, http://192.168.0.50:5000/open_sesame. 

### If using `openDoorCookies.py`:
Using `nano`, `vim`, or any other text editor, replace the following values for their appropriate keys with the associated cookies: 
- For `"PHPSESSID":`, replace "php_sess_id" with the appropriate cookie value

## Apple Shortcut:
Download the `unlockDoor.shortcut` file to your iOS device using/clicking the QR code or link below: <br>

<a href="https://raw.githubusercontent.com/dekay7/CBORDDoorUnlock/main/unlockDoor.shortcut"><img src="unlockDoorShortcut.png" alt="unlockDoor.shortcut download link QR code" width="50%" height="auto"></a><br>
Apple Shortcut Download Link: https://raw.githubusercontent.com/dekay7/CBORDDoorUnlock/main/unlockDoor.shortcut <br>

### Shortcut Configuration:
When prompted to enter a URL, replace the default value, `http://192.168.0.50:5000/open_sesame`, with the local IP of the host server, followed by the port, and the subdirectory.
