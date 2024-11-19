#!/bin/sh

set -eu

usage="usage: $(basename "$0") [-d os_base_disk_location_qcow2] [-q number_queues_need] [-s ssh_guest_port]"

create_bridge_if_not_exist(){
	for interface in $(ip -json addr show | jq '.[].ifname | contains("br0")'); do
		if [[ "$interface" == "true" ]]; then
			return
		fi
	done
	ip link add br0 type bridge && ip link set br0 up
}

create_test_environ() {
	(( vectors="$2"*2+2 ))
	qemu-system-x86_64 -daemonize -enable-kvm -machine q35 -device intel-iommu -cpu host -m 1024 "$1" -device virtio-net,netdev=net0,mac=$(printf 'DE:AD:BE:EF:%02X:%02X\n' $((RANDOM%256)) $((RANDOM%256))),mq=on,vectors="$vectors" -netdev tap,id=net0,queues="$2",vhost=on,script=$(dirname $0)/qemu-ifup.sh -nic user,hostfwd=tcp::"$3"-:22
}

create_linked_clone_qcow2() {
	COUNT=1
	for count in $(find -type f -iname "$1"); do  
		if [[ ! -f clone_"$COUNT"_"$1" ]]; then
			qemu-img create -f qcow2 -F qcow2 -b "$1" clone_"$COUNT"_"$1"
		fi
	done
}

summon_ansible() {
	# Need VM to boot before provision with ansible over ssh
	for sec in {1..15}; do
		echo -n "."
		sleep 1
	done
	ansible-playbook -i ansible/staging.yml ansible/site.yml
}

if [[ $(id -u) -ne 0 ]] ; then 
	echo "Run this script as root"
	exit 1
fi

while getopts ":d:q:s:" opt; do
    case $opt in
        d)
            disk_location="$OPTARG"
            ;;
        q)
            queues_number="$OPTARG"
            ;;
        s)
            ssh_port="$OPTARG"
            ;;
        :)
            printf "missing argument for -%s\n" "$OPTARG" >&2; echo "$usage" >&2; exit 1
            ;;
        \?)
            printf "illegal option: -%s\n" "$OPTARG" >&2; echo "$usage" >&2; exit 1
            ;;
    esac
done

if [ ! "$disk_location" ] || [ ! "$queues_number" ] || [ ! "$ssh_port" ] ; then
	echo "arguments -d, -q, s must be provided"
	echo "$usage" >&2; exit 1
fi

shift $((OPTIND-1))

create_bridge_if_not_exist

create_linked_clone_qcow2 "$disk_location"

for vm_disk in $(find -type f -iname "clone_[[:digit:]]_$disk_location"); do
	create_test_environ "$vm_disk" "$queues_number" "$ssh_port"
	(( ssh_port++ ))
done

summon_ansible
