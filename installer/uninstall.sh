set -e

tput setaf 5
echo "Checking your system..."

if [[ -f "/etc/systemd/system/dnsfallbackd.service" ]]; then
  tput setaf 2
  echo "dnsfallbackd is installed on this device. Proceeding..."
else
  tput setaf 1
  echo "dnsfallbackd isn't installed on your device. Exiting..."
  exit
fi

tput setaf 3
echo -n "Do you really want to uninstall dnsfallbackd? [Y/n]: "
read proceed

if [ "$proceed" == "" ] || [ "$proceed" == "y" ] || [ "$proceed" == "Y" ]; then
  tput setaf 5
  echo "> pip uninstall dnsfallbackd"
  tput setaf 7
  pip uninstall dnsfallbackd
  
  echo ""
  
  tput setaf 5
  echo "> rm /etc/dnsfallbackd -rf"
  tput setaf 7
  rm /etc/dnsfallbackd -rf
  
  echo ""
  
  tput setaf 5
  echo "> rm /etc/systemd/system/dnsfallbackd.service -f"
  tput setaf 7
  rm /etc/systemd/system/dnsfallbackd.service -f
  
  echo ""
  
  tput setaf 2
  echo "Done!"
else
  tput setaf 1
  echo "Aborting..."
fi
