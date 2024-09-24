# CBORD MobileID/CardAdmin Door Opener
Due to this program's reliance on [Playwright](https://playwright.dev/python/), the recommended deployment method is through [Docker](#docker-installation-linux-macos-windows). The [Native (Manual) installation](#native-manual-installation-debianubuntu-macos-windows) is only compatible with Debian/Ubuntu, macOS, and Windows.

## ⚠️DISCLAIMER:
Any malicious use of this program is not the responsibility of the author. By downloading and using this program, you agree that you, and any other parties involved in your implementation of this program, are entirely responsible for its use/misuse. <br>
**Please do not do stupid shit.** The goal of this program is to provide an alternate method of room access as a quality of life improvement. No malicious intent exists behind the development of this program. 

## Docker Installation (Linux, macOS, Windows):
Make sure you have Docker already installed on your device (that will be acting as the server). <br>
Download `CBORD_Docker.zip` from the [latest release](https://github.com/dekay7/CBORDDoorUnlock/releases/latest). To do this from the command line, copy the link address of `CBORD_Docker.zip` and use the following command (be sure to replace `paste_copied_link_here` with the copied link):
```bash
wget paste_copied_link_here
```
Then, unzip the binary using the following command:
```bash
unzip CBORD_Docker.zip
```
Using `nano`, `vim`, or any other text editor, assign the following variables in `Dockerfile` to the appropriate values:
- For `ENV LOGINUSER=`, replace "oktausername1" with your OKTA username
- For `ENV PASS=`, replace "okta_p@ssword" with your OKTA password
- For `LOGINURL=`, replace "https://cardadmin.iit.edu/login/ldap.php" with the login address for your CardAdmin interface
- For `DOORURL=`, replace "https://cardadmin.iit.edu/student/openmydoor.php" with the open my door endpoint for your CardAdmin interface

Open a terminal in the same directory as the `docker-compose.yml` file and install using the following command:
```bash
docker-compose up --build -d
```
If you choose to change the environment variables later, make your edits, save, then use the command:
```bash
docker-compose down && docker-compose up -d
```
Once complete, go to the [Apple Shortcut](#apple-shortcut) section to install the shortcut to your iPhone. 

#### Optional:
If you would like receive emails every time your door is unlocked, assign the following variables in `.env` to the appropriate values:
- For `SENDER=`, replace "senderemail@gmail.com" with a sender Gmail to receive door unlock notifications from
- For `APPPASS=`, replace "aaaa bbbb cccc dddd" with:
    - Your Gmail password **(if you <u>ARE NOT</u> using 2FA)**
    - A generated app password **(if you <u>ARE</u> using 2FA)**

## Native (Manual) Installation (Debian/Ubuntu, macOS, Windows):
Download `CBORD_Manual.zip` from the [latest release](https://github.com/dekay7/CBORDDoorUnlock/releases/latest).
Using `nano`, `vim`, or any other text editor, assign the following variables in `.env` to the appropriate values:
- For `LOGINUSER=`, replace "oktausername1" with your OKTA username
- For `PASS=`, replace "okta_p@ssword" with your OKTA password
- For `LOGINURL=`, replace "https://cardadmin.iit.edu/login/ldap.php" with the login address for your CardAdmin interface
- For `DOORURL=`, replace "https://cardadmin.iit.edu/student/openmydoor.php" with the open my door endpoint for your CardAdmin interface

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
