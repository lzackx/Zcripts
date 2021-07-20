#!/bin/sh

set -e
set -x

# Pull Resources
sudo apt install git

mkdir -p ~/Repositories
cd ~/Repositories
git clone https://github.com/lzackx/Zcripts.git

if [ ! -d Zcripts ];then
    exit 1;
fi

cd Zcripts
sudo cp ./rpi/omv.hosts /etc/hosts

cd ~/Repositories
mkdir apc
cd apc
wget https://udomain.dl.sourceforge.net/project/apcupsd/apcupsd%20-%20Stable/3.14.14/apcupsd-3.14.14.tar.gz

cd ~/Repositories
sudo apt update
sudo apt upgrade -y

# Installation
sudo apt install vlc-bin -y

sudo apt install vim -y
cp ~/Repositories/Zcripts/zevn/.vimvc ~/

# zsh
sudo apt install zsh -y
wget -O - https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh | sudo bash
cp ~/Repositories/Zcripts/zevn/.zevn ~/

# OpenMediaVault
wget -O - https://github.com/OpenMediaVault-Plugin-Developers/installScript/raw/master/install | sudo bash

#sudo omv-salt deploy run