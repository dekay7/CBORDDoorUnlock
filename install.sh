#!/bin/bash
ip_address=$(ip -o route get to 1.1.1.1 | sed -n 's/.*src \([0-9.]\+\).*/\1/p')
os=$(uname -s)
case "$os" in
  Linux)
    # Debian/Ubuntu
    if command -v apt &> /dev/null; then
      sudo apt update
      sudo apt install -y unzip git jq qrencode catimg
    # Red Hat/CentOS
    elif command -v yum &> /dev/null; then
      sudo yum -y install unzip git jq qrencode catimg
    # Fedora
    elif command -v dnf &> /dev/null; then
      sudo dnf install --assumeyes unzip git jq qrencode catimg
    else
      echo "Unsupported Linux distribution."
    fi
    ;;
  Darwin)
    # macOS (using Homebrew)
    if command -v brew &> /dev/null; then
      brew install unzip
      brew install git
      brew install jq
      brew install qrencode
      brew install catimg
    else
      echo "Homebrew is not installed. Please install Homebrew first."
      exit 1
    fi
    ;;
  *)
    echo "Unsupported operating system."
    exit 1
    ;;
esac
release_info=$(curl -s "https://api.github.com/repos/dekay7/CBORDDoorUnlock/releases/latest")
download_url=$(echo "$release_info" | jq -r '.assets[0].browser_download_url')
wget --progress=bar:force:noscroll $download_url
wait $1
unzip open_door.zip -d open_door
rm open_door.zip
cd open_door/
sudo mv openDoor.service /etc/systemd/system
sudo systemctl enable openDoor.service
sudo systemctl start openDoor.service
sudo systemctl status openDoor.service
mv example.env .env
env_file=".env"
show_form() {
  username=$(whiptail --inputbox "Enter IIT username (without @hawk.iit.edu):" 8 50 "$USERNAME" 3>&1 1>&2 2>&3)
  password=$(whiptail --passwordbox "Enter IIT password:" 8 50 "$PASSWORD" 3>&1 1>&2 2>&3)
  sender=$(whiptail --inputbox "(OPTIONAL) Enter sender email address (for email notifications)\nPress enter/return to skip:" 8 50 "$SENDER" 3>&1 1>&2 2>&3)

  if [ -n "$sender" ]; then
      apppass=$(whiptail --inputbox "Enter APPPASS:" 8 50 "$APPPASS" 3>&1 1>&2 2>&3 || echo "")
  fi
}
source "$env_file"
show_form
sed -i "s/^USERNAME=.*/USERNAME=$username/" "$env_file"
sed -i "s/^PASSWORD=.*/PASSWORD=$password/" "$env_file"
if [ -n "$sender" ]; then
  sed -i "s/^SENDER=.*/SENDER=$sender/" "$env_file"
fi
if [ -n "$apppass" ]; then
  sed -i "s/^APPPASS=.*/APPPASS=$apppass/" "$env_file"
fi
echo "USERNAME: $username"
echo "PASSWORD: $password"
echo "SENDER: ${sender:-Not provided}"
echo "APPPASS: ${apppass:-Not provided}"
echo "Your door can be opened by visiting the following link: http://$ip_address:5000/open_sesame"
echo "Download the Apple Shortcut to your iPhone using the following URL:"
catimg unlockDoorShortcut.png
rm unlockDoorShortcut.png
echo "Completed installation. Enjoy!"