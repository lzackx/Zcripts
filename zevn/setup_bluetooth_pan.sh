#!/bin/sh

set -e

echo "reference: https://leux.cn/doc/Raspberry%E9%80%9A%E8%BF%87%E8%93%9D%E7%89%99SSH.html"
echo "\$*: $*"

while getopts ":a:h" opt
do
    # echo "OPTIND: $OPTIND"
    # echo "OPTARG: $OPTARG"
    case $opt in
        h)
            echo "setup pan0 for bluetooth"
            echo "default pan0 gateway address: 192.168.69.1/24"
            ;;
        ?)
            echo "there is unrecognized parameter."
            exit 1
            ;;
    esac
done

# set -x

echo '=== use super user ==='
sudo su

echo '=== install dependencies ==='
apt install bluez bluez-firmware bluez-tools dnsmasq
echo '=== dependencies installed ==='

echo '=== create pan0 ==='
cat << EOF > /etc/systemd/network/pan0.netdev
[NetDev]
Name=pan0
Kind=bridge
EOF

echo '=== setup pan0 ==='
cat << EOF > /etc/systemd/network/pan0.network
[Match]
Name=pan0
[Network]
Address=192.168.69.1/24
DHCPServer=yes
EOF

echo '== create bluetooth agent service ==='
cat << EOF > /etc/systemd/system/bt-agent.service
[Unit]
Description=Bluetooth Auth Agent

[Service]
ExecStart=/bin/bt-agent -c NoInputNoOutput
Type=simple

[Install]
WantedBy=multi-user.target
EOF

echo '=== setup bluetooth network service ==='
cat << EOF > /etc/systemd/system/bt-network.service
[Unit]
Description=Bluetooth NEP PAN
After=pan0.network

[Service]
ExecStart=/bin/bt-network -s nap pan0
Type=simple

[Install]
WantedBy=multi-user.target
EOF

echo '=== setup dnsmasq (/etc/dnsmasq.conf) ==='
cat << EOF >> /etc/dnsmasq.conf
interface=pan0
listen-address=192.168.69.1
server=8.8.8.8
dhcp-range=192.168.69.100,192.168.69.200,255.255.255.0,24h
EOF

echo '=== enable service ==='
systemctl enable bluetooth
systemctl enable systemd-networkd
systemctl enable bt-agent
systemctl enable bt-network
systemctl enable dnsmasq