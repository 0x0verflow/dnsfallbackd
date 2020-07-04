# This makefile is presented to you by the best developer in the world: trueFireblade aka Annie!
# But even though I put the stuff into the makefile its a slight modification of 0x0verflows installscript so if you find any errors blame him, thx <3

install:
	set -e
	tput setaf 5
	echo "Checking your system..."
	if [[ -f "/bin/apt" ]]; then
	  tput setaf 2
	  echo "Your system is using apt as package manager! Proceeding..."
	  PMANAGER = "apt"
	elif  [[ -f "/bin/pacman" ]]; then
	  tput setaf 2
	  echo "Your system is using pacman as package manager! Proceeding..."
	  PMANAGER = "pacman"
	else
	  tput setaf 1
	  echo "Seems like your system is incompatible with this install-script. You can try to install dnsfallbackd manually. Exiting..."
	  exit
	fi

	tput setaf 3
	echo -n "You're about to install dnsfallbackd on your system including all dependencies (python3.6, git, pyping[pip], requests[pip]). Proceed? [Y/n]: "
	read proceed

	if [ "$proceed" == "" ] || [ "$proceed" == "y" ] || [ "$proceed" == "Y" ]; then
	  # --- Getting system up to date
	  tput setaf 5
	  if [[ $PMANAGER == "apt" ]]; then
	    echo "> apt-get update"
	    tput setaf 7
	    apt-get update

	    echo ""

	    tput setaf 5
	    echo "> apt-get upgrade"
	    tput setaf 7
	    apt-get upgrade
	  elif [[ $PMANAGER == "pacman" ]]; then
	    echo "> pacman -Syu"
	    tput setaf 7
	    pacman -Syu
	  fi
	  echo ""

	  # --- Installing dnsfallbackd ---
	  tput setaf 5
	  if [[ $PMANAGER == "apt" ]]; then
	    echo "> apt-get install python3.6 git"
	    tput setaf 7
	    apt-get install python3.6 git
	  elif [[ $PMANAGER == "pacman" ]]; then
	    echo "> pacman -S python git"
	    tput setaf 7
	    pacman -S python git
	  fi

	  echo ""

	  tput setaf 5
	  echo "> mkdir ./tmp/"
	  tput setaf 7
	  mkdir ./tmp/

	  echo ""

	  tput setaf 5
	  echo "> git clone --depth=1 https://github.com/0x0verflow/dnsfallbackd.git"
	  tput setaf 7
	  git clone --depth=1 https://github.com/0x0verflow/dnsfallbackd.git

	  echo ""

	  tput setaf 5
	  echo "> python3 ./dnsfallbackd-master/setup.py"
	  tput setaf 7
	  python3 ./dnsfallbackd-master/setup.py

	  echo ""

	  tput setaf 5
	  echo "> rm -rf ./dnsfallbackd-master/"
	  tput setaf 7
	  rm -rf ./dnsfallbackd-master/

	  echo ""

	  # --- Service ---
	  tput setaf 5
	  echo "Installing service to /etc/systemd/system/dnsfallbackd.service..."
	  tput setaf 7

	  adduser dnsfallbackd --no-create-home --disabled-login --disabled-password --shell "/bin/false" --gecos ""

	  touch /etc/systemd/system/dnsfallbackd.service

	  echo "[Unit]" >> /etc/systemd/system/dnsfallbackd.service
	  echo "Description=Decentralized daemon to keep your services always accessable through Cloudflare DNS or custom DNS through userscripts" >> /etc/systemd/system/dnsfallbackd.service
	  echo "" >> /etc/systemd/system/dnsfallbackd.service
	  echo "[Service]" >> /etc/systemd/system/dnsfallbackd.service
	  echo "Type=simple" >> /etc/systemd/system/dnsfallbackd.service
	  echo "ExecStart=dnsfallbackd" >> /etc/systemd/system/dnsfallbackd.service
	  echo "User=dnsfallbackd" >> /etc/systemd/system/dnsfallbackd.service
	  echo "" >> /etc/systemd/system/dnsfallbackd.service
	  echo "[Install]" >> /etc/systemd/system/dnsfallbackd.service
	  echo "WantedBy=multi-user.target" >> /etc/systemd/system/dnsfallbackd.service

	  systemctl enable dnsfallbackd
	  systemctl start dnsfallbackd

	  tput setaf 2
	  echo "Done! Start and stop dnsfallbackd using 'systemctl start/stop dnsfallbackd'! Configuration files are located at /etc/dnsfallbackd/!"
	 else
	  tput setaf 1
	  echo "Aborting..."
	 fi

uninstall:
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

