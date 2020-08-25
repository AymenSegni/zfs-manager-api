#!/bin/bash
red=`tput setaf 2`
reset=`tput sgr0`
kernel=$(uname -r)
echo "${red}Running: apt-get install linux-headers-$kernel -y${reset}"
apt-get install linux-headers-"$kernel" -y
echo "${red}Running: apt-get install software-properties-common -y${reset}"
apt-get install software-properties-common -y
echo "${red}Running: apt-add-repository --yes ppa:zfs-native/stable${reset}"
apt-add-repository --yes ppa:zfs-native/stable
echo "${red}Running: apt-get update${reset}"
apt-get update
echo "${red}Running: apt-get install spl-dev spl-dkms zfs-dkms -y${reset}"
apt-get install spl-dev spl-dkms zfs-dkms -y
echo "${red}Running: apt-get install ubuntu-zfs -y${reset}"
apt-get install ubuntu-zfs -y
echo "${red}Running: dpkg-reconfigure spl-dkms${reset}"
dpkg-reconfigure spl-dkms
echo "${red}Running: dpkg-reconfigure zfs-dkms${reset}"
dpkg-reconfigure zfs-dkms
echo "${red}Running: modprobe zfs${reset}"
modprobe zfs
echo "${red}Running: lsmod | grep zfs${reset}"
lsmod | grep zfs
echo "${red}Setting up zpool to automatically import pools${reset}"
sed -i '/^.*modprobe zfs zfs_autoimport_disable.*$/c\\t modprobe zfs zfs_autoimport_disable=0' /etc/init/zpool-import.conf
sed -i '/^.*exit 0.*$/c\\zfs mount -a' /etc/rc.local
echo "exit 0" >> /etc/rc.local
echo "${red}Done!${reset}"