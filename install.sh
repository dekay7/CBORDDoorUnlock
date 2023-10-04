#!/bin/bash

ip_address=$(ip -o route get to 1.1.1.1 | sed -n 's/.*src \([0-9.]\+\).*/\1/p')
os=$(uname -s)

# Check for the existence of /etc/os-release
if [ -e /etc/os-release ]; then
    # Source the os-release file to get the ID variable
    . /etc/os-release
    case "$ID" in
        debian|ubuntu)
            sudo apt update
            sudo apt install -y wget unzip git jq python3 python3-pip whiptail
            ;;
        centos|rhel)
            sudo yum -y install wget unzip git jq python3 python3-pip newt
            ;;
        fedora)
            sudo dnf install --assumeyes wget unzip git jq python3 python3-pip newt
            ;;
        *)
            echo "Unsupported Linux distribution."
            exit 1
            ;;
    esac
elif [ "$os" == "Darwin" ]; then
    # macOS (using Homebrew)
    if command -v brew &> /dev/null; then
        brew install wget unzip git jq python3 newt
    else
        echo "Homebrew is not installed. Please install Homebrew first."
        exit 1
    fi
else
    echo "Unsupported operating system."
    exit 1
fi

release_info=$(curl -s "https://api.github.com/repos/dekay7/CBORDDoorUnlock/releases/latest")
download_url=$(echo "$release_info" | jq -r '.assets[0].browser_download_url')
wget --progress=bar:force:noscroll -O open_door.zip "$download_url"
unzip open_door.zip -d open_door
rm open_door.zip
cd open_door/

# Check for the presence of either venv or virtualenv
if command -v python3 -m venv &> /dev/null; then
    python3 -m venv venv
elif command -v python3 -m virtualenv &> /dev/null; then
    python3 -m virtualenv venv
else
    echo "Could not find venv or virtualenv. Please install either venv or virtualenv and rerun the script."
    exit 1
fi

source venv/bin/activate
pip3 install -r requirements.txt
playwright install-deps
playwright install
deactivate
current_dir=$(pwd)
sed -i "s|'/root/open_door/venv/bin/python3'|'$current_dir/venv/bin/python3'|" openDoorServer.py
sed -i "s|'/root/open_door/openDoor.py'|'$current_dir/openDoor.py'|" openDoorServer.py
sed -i "s|'WorkingDirectory=/root/open_door/'|WorkingDirectory=$current_dir|" openDoor.service
sed -i "s|ExecStart=/root/open_door/venv/bin/python3 openDoorServer.py|ExecStart=$current_dir/venv/bin/python3 openDoorServer.py|" openDoor.service
sudo ln openDoor.service /etc/systemd/system/openDoor.service
sudo systemctl enable openDoor.service
sudo systemctl start openDoor.service
mv example.env .env
env_file=".env"
show_form() {
  username=$(whiptail --inputbox "Enter IIT username (without @hawk.iit.edu):" 8 50 "$USERNAME" 3>&1 1>&2 2>&3)
  password=$(whiptail --passwordbox "Enter IIT password:" 8 50 3>&1 1>&2 2>&3)
  sender=$(whiptail --inputbox "(OPTIONAL) Enter sender email address (for email notifications)\nPress enter/return to skip:" 8 50 3>&1 1>&2 2>&3)

  if [ -n "$sender" ]; then
      apppass=$(whiptail --inputbox "Enter APPPASS:" 8 50 3>&1 1>&2 2>&3 || echo "")
  fi
}
source "$env_file"
show_form
escaped_username=$(printf "%s\n" "$username" | sed 's/[&/]/\\&/g')
sed -i "s|^USERNAME=.*|USERNAME=$escaped_username|" "$env_file"
escaped_password=$(printf "%s\n" "$password" | sed 's/[&/]/\\&/g')
sed -i "s|^PASSWORD=.*|PASSWORD=$escaped_password|" "$env_file"
if [ -n "$sender" ]; then
  sed -i "s/^SENDER=.*/SENDER=$sender/" "$env_file"
fi
if [ -n "$apppass" ]; then
  sed -i "s/^APPPASS=.*/APPPASS=$apppass/" "$env_file"
fi
whiptail --title "Information" --msgbox \
"USERNAME: $username
PASSWORD: [HIDDEN]
SENDER: ${sender:-Not provided}
APPPASS: ${apppass:-Not provided}
Your door can be opened by visiting the following link: http://$ip_address:5000/open_sesame
Download the Apple Shortcut to your iPhone using the following URL:
https://raw.githubusercontent.com/dekay7/CBORDDoorUnlock/main/unlockDoor.shortcut" 20 70

# Ask the user to reboot
if whiptail --title "Reboot Confirmation" --yesno "Reboot? (Necessary)" 10 50; then
    reboot
else
    whiptail --msgbox "To ensure everything works properly, you must reboot your host. Please reboot manually later. " 10 50
fi