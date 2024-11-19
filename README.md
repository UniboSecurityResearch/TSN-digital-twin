<!--
    Copyright (C) 2024 Lorenzo Rinieri, Andrea Giovine, Andrea Melis

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>. 
-->

# # TSN-digital-twin
This repository contains the artifacts for the paper "Time-Sensitive Networking Digital Twin for STRIDE-based Security Testing".

# Instructions for Configuring and Running the System

## Prerequisites

The `qemu-system` is compiled with `vde2`. To make it work, you need to create symbolic links and set up the environment:

### Symbolic Links
Create the following symbolic links:
```bash
ln -s libvdeplug4/libvdeplug_ptp.so libvdeplug_ptp.so
ln -s libvdeplug4/libvdeplug.so libvdeplug.so.3
```

### Using the New Compiled Library
Set the `LD_LIBRARY_PATH` to the path of the compiled `vde4` library:
```bash
export LD_LIBRARY_PATH=<path_to_compiled_vde4>
```

## Running QEMU

Run the QEMU system with the following command:
```bash
LD_LIBRARY_PATH=. qemu-system-x86_64 -enable-kvm -machine q35 -cpu host -device intel-iommu -m 512     -drive file=/home/gio/tesi/clone_debian_disk.qcow2,format=qcow2     -net nic,macaddr=52:54:00:11:22:11 -net vde,sock=ptp://
```

## Network Configuration

### Using `ptp4l`
```bash
sudo ptp4l -H -2 -E -i enp0s31f6 -m
```

### Creating a Clone Disk
```bash
qemu-img create -f qcow2 -F qcow2 -b debian_disk.qcow2 clone#_debian_disk.qcow2
```

### Creating and Setting Up a Bridge
```bash
ip link add br0 type bridge && ip link set br0 up
```

### Daemonizing QEMU
```bash
qemu-system-x86_64 -daemonize -enable-kvm -machine q35 -device intel-iommu -cpu host -m 1024     -drive file=clone1_debian_disk.qcow2     -device virtio-net,netdev=net0,mac=$(printf 'DE:AD:BE:EF:%02X:%02X
' $((RANDOM%256)) $((RANDOM%256))),mq=on,vectors=10     -netdev tap,id=net0,queues=4,vhost=on,script=/home/gio/tesi/qemu-ifup.sh     -nic user,hostfwd=tcp::60022-:22
```

## Configuring Ethernet and Traffic Shaping

### Adjusting Ethernet Settings
```bash
ethtool -L enp0s3 combined 4
```

### Creating a Queue Discipline with `tc-cbs`
```bash
sudo tc qdisc add dev "$1" parent root handle 6666 mqprio     num_tc 3     map 2 2 1 0 2 2 2 2 2 2 2 2 2 2 2 2     queues 1@0 1@1 2@2     hw 0
```

### Configuring CBS Queues
Queue 1:
```bash
tc qdisc replace dev "$1" parent 6666:1 cbs idleslope 98688 sendslope -901312 hicredit 153 locredit -1389 offload 0
```

Queue 2:
```bash
tc qdisc replace dev "$1" parent 6666:2 cbs idleslope 3648 sendslope -996352 hicredit 12 locredit -113 offload 0
```

### Configuring `iptables`
```bash
iptables -t mangle -A POSTROUTING -p udp --sport 7777 -j CLASSIFY --set-class 6666:2
iptables -t mangle -A POSTROUTING -p udp --dport 7777 -j CLASSIFY --set-class 6666:2

iptables -t mangle -A POSTROUTING -p udp --dport 6666 -j CLASSIFY --set-class 6666:3
iptables -t mangle -A POSTROUTING -p udp --sport 6666 -j CLASSIFY --set-class 6666:3
```

## Testing Network Performance

### Using `iperf`
#### Server
```bash
iperf3 -s -p 7777
```

#### Client
```bash
iperf3 -c 192.168.1.35 --udp -p 7777 -b 1T
```

### Generating Traffic with `hping3`
```bash
hping3 --udp --flood 192.168.1.35 --destport 6666 -d 512
```

# Cite us
If you find this work interesting and use it in your academic research, please cite our paper!

[![DOI](https://zenodo.org/badge/890696790.svg)](https://doi.org/10.5281/zenodo.14187717)

