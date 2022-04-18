[TOC]





# Trick



## Create a KVM Guest using Virsh

### Check whether Virtualization is enabled

```shell
egrep -c '(vmx|svm)' /proc/cpuinfo
kvm-ok
sudo apt install -y cpu-checker
```

### Install KVM, Qemu, virt-manager & libvirtd daemon
```shell
sudo apt install -y qemu qemu-kvm libvirt-daemon libvirt-daemon-system bridge-utils virt-manager
lsmod | grep kvm
sudo systemctl status libvirtd.service
```

### Create a virtual machine from the command line
```shell
virt-install --name=linuxconfig-vm \
--vcpus=1 \
--memory=1024 \
--cdrom=/tmp/debian-9.0.0-amd64-netinst.iso \
--disk size=5 \
--os-variant=debian8
```



```shell
root@kvmhost /tmp> virt-install \
--network bridge:br0 \
--name testmachine \
--ram=128 \
--vcpus=1 \
--disk path=/var/lib/libvirt/images/testmachine.img,size=0.2 \
--nographics \
--location /tmp/Core-current.iso \
--extra-args "console=ttyS0"

osinfo-query os

virsh list --all

virsh edit linuxconfig-vm
```



## Delete a KVM Guest Using Virsh

### List all a VM guests
```shell
virsh list
virsh list --all
```

```shell
virsh dumpxml VM_NAME
virsh dumpxml --domain VM_NAME
```

```shell
virsh dumpxml --domain openbsd | grep 'source file'
```

### Shutdown the guest
```shell
virsh shutdown VM_NAME
virsh shutdown --domain VM_NAME
```

### force a guest virtual machine to stop
```shell
virsh destroy VM_NAME
virsh destroy --domain VM_NAME
```
### Deleting a virtual machine



```shell
virsh undefine VM_NAME
virsh undefine --domain VM_NAME

m -rf /nfswheel/kvm/openbsd.qcow2
```

* A note about error: “cannot delete inactive domain with snapshots”
```shell
virsh snapshot-list --domain VM_NAME
virsh snapshot-delete --domain VM_NAME --snapshotname
```

* Remove associated VM storage volumes and snapshots while undefineing a domain/VM
```shell
virsh undefine --domain {VM_NAME_HERE} --storage

virsh domblklist --domain {VM_NAME_HERE}
virsh snapshot-list --domain {VM_NAME_HERE}

virsh undefine --domain {VM_NAME_HERE} --remove-all-storage

virsh undefine --domain {VM_NAME_HERE} --delete-snapshots

virsh undefine --domain mysql-server --remove-all-storage

virsh undefine --domain mysql-server --remove-all-storage 
```





# Cookbook

## Getting start

### Install QEMU from packages

```shell
sudo apt-get update -y
sudo apt-get install -y qemu

dpkg --list | grep qemu
```

### Managing disk images with qemu-img
```shell
qemu-img -h | grep Supported

qemu-img create -f raw debian.img 10G
ls -lah debian.img
file -s debian.img
qemu-img info debian.img
```



### Preparing images for OS installation with qemu-nbd

* outlined to partition and create a filesystem on the blank image:

* associate the blank image file
```shell
modprobe nbd
qemu-nbd --format=raw --connect=/dev/nbd0 debian.img 
```

* Create two partitions on the block device. swap,root partition
```shell
sfdisk /dev/nbd0 << EOF 
,1024,82; 
EOF 

ls -la /dev/nbd0*
mkswap /dev/nbd0p1
mkfs.ext4 /dev/nbd0p2
modinfo nbd

file -s /dev/nbd0
file -s debian.img
```



### Installing a custom OS on the image with debootstrap

```shell
sudo apt install -y debootstrap

sudo mount /dev/nbd0p2 /mnt/kvm-os
mount | grep mnt

sudo debootstrap --arch=amd64 --include="openssh-server vim" stable /mnt/kvm-os http://httpredir.debian.org/debian/
 ls -lah /mnt/kvm-os
 
 mount --bind /dev/ /mnt/kvm-os/dev
 ls -la /mnt/kvm-os/dev/ | grep nbd0 
 sudo chroot /mnt/
 pwd
 cat /etc/debian_version
 mount -t proc none /proc
 mount -t sysfs none /sys
 apt-get install -y --force-yes linux-image-amd64 grub2
 grub-install /dev/nbd0 --force
 update-grub2
 passwd
 echo "pts/0" >> /etc/securetty
 systemctl set-default multi-user.target
 echo "/dev/sda2 / ext4 defaults,discard 0 0" > /etc/fstab
 umount /proc/ /sys/ /dev/
 exit
 
 grub-install /dev/nbd0 --root-directory=/mnt/kvm-os/ --modules="biosdisk part_msdos" --force
 sed -i 's/nbd0p2/sda2/g' /mnt/kvm-os/boot/grub/grub.cfg 
 umount /mnt/kvm-os/
 qemu-nbd --disconnect /dev/nbd0 
```



### Resizing an image

```sh
apt install kpartx

qemu-img info debian.img
qemu-img resize -f raw debian.img +10GB
qemu-img info debian.img
```



print the name of the first unused loop device:

```shell
losetup -f
```

> /dev/loop0

```she
losetup /dev/loop1 debian.img
```



Read the partition information from the associated loop device and create device mappings:

```shell
# Read the partition information from the associated loop device
kpartx -av /dev/loop1

# Representing the partitions on the raw image:
ls -la /dev/mapper

# Obtain some information from the root partition mapping:
tune2fs -l /dev/mapper/loop1p2

# Check the filesystem on the root partition of the mapped device:
e2fsck /dev/mapper/loop1p2 

# Remove the journal from the root partition device:
tune2fs -O ^has_journal /dev/mapper/loop1p2

# Ensure that the journaling has been removed:
tune2fs -l /dev/mapper/loop1p2 | grep "features"

# Remove the partition mapping:
kpartx -dv /dev/loop1

# Detach the loop device from the image:
losetup -d /dev/loop1

# Associate the raw image with the network block device:
qemu-nbd --format=raw --connect=/dev/nbd0 debian.img

# List the available partitions
fdisk /dev/nbd0
p
d
n
p
2
w

# Associate the first unused loop device with the raw image file
losetup /dev/loop1 debian.img

# Read the partition information from the associated loop device and create the device mappings
kpartx -av /dev/loop1

# perform a filesystem check
e2fsck -f /dev/mapper/loop1p2
 
# Resize the filesystem on the root partition of the mapped device:
resize2fs /dev/nbd0p2

# Create the filesystem journal because we removed it earlier
tune2fs -j /dev/mapper/loop1p2

# Remove the device mappings
kpartx -dv /dev/loop1
losetup -d /dev/loop1
```



### Using pre-existing images

```shell
 wget https://people.debian.org/~aurel32/qemu/amd64/debian_wheezy_amd64_standard.qcow2
 wget https://cdimage.debian.org/cdimage/openstack/archive/9.3.0/debian-9.3.0-openstack-amd64.qcow2
 
 qemu-img info debian-9.3.0-openstack-amd64.qcow2
```



### Running virtual machine with qemu-system-*

```shell
# list binaries file you have
ls -la /usr/bin/qemu-system-*

# what CPU architectures QEMU supports on the host system: 
qemu-system-x86_64 --cpu help

# Start a new QEMU virtual machine using the x86_64 CPU architecture
qemu-system-x86_64 \
-name debian -vnc 146.20.141.254:0 \
-cpu Nehalem \
-m 1024 \
-drive format=raw,index=2,file=debian.img \
-daemonize

# Ensure that the instance is running
pgrep -lfa qemu

# Terminate the Debian QEMU instance
sudo pkill qemu

```



### Starting the QEMU VM with KVM support

````shell
cat /proc/cpuinfo | egrep "vmx|svm" | uniq

modprobe kvm

# Start a QEMU instance with KVM support
sudo qemu-system-x86_64 -name debian -vnc 192.168.122.1:0 -m 1024 -drive format=raw,index=2,file=debian.img -enable-kvm -daemonize

# Ensure that the instance is running: 
pgrep -lfa qemu

# Terminate the instance
pkill qemu
````



### Connecting to a running instance with VNC

```shell
# Start a new KVM-accelerated qemu instance:
sudo qemu-system-x86_64 -name debian -vnc 192.168.122.1:0 -m 1024 -drive format=raw,index=2,file=debian.img -enable-kvm -daemonize

# Ensure that the instance is running: 
pgrep -lfa qemu

# Start the VNC client and connect to the VNC server on the IP address and display
port you specified in step 1
```



## Install and configuring libvirt

````shell
# install the package
sudo apt update && apt install libvirt-bin

# Ensure that the libvirt daemon is running
pgrep -lfa libvirtd

# Examine the default configuration: 
cat /etc/libvirt/libvirtd.conf | grep -vi "#" | sed '/^$/d'

# Disable the security driver in QEMU 
vim /etc/libvirt/qemu.conf
security_driver = "none"

# Restart the libvirt daemon: 
sudo /etc/init.d/libvirt-bin restart

# Examine all configuration files in the libvirt directory:
ls -la /etc/libvirt/
````



### Defining KVM instances by XML file

```shell
# List all virtual machines
 virsh list --all
```



```xml
 vim kvm1.xml
<domain type='kvm' id='1'>
	<name>kvm1</name>
    <memory unit='KiB'>1048576</memory>
    <vcpu placement='static'>1</vcpu>
    <os>
        <type arch='x86_64' machine='pc-i440fx-trusty'>hvm</type>
        <boot dev='hd'/>
    </os>
    <on_poweroff>destroy</on_poweroff>
    <on_reboot>restart</on_reboot>
    <on_crash>restart</on_crash>
    <devices>
        <emulator>/usr/bin/qemu-system-x86_64</emulator>
        <disk type='file' device='disk'>
        	<driver name='qemu' type='raw'/>
        	<source file='./debian.img'/>
        	<target dev='hda' bus='ide'/>
        	<alias name='ide0-0-0'/>
        	<address type='drive' controller='0' bus='0' target='0' unit='0'/>
        </disk>
        <interface type='network'>
            <source network='default'/>
            <target dev='vnet0'/>
            <model type='rtl8139'/>
            <alias name='net0'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
        </interface>
        <graphics type='vnc' port='5900' autoport='yes' listen='192.168.122.1'>
            <listen type='address' address='192.168.122.1'/>
        </graphics>        
    </devices>
    <seclabel type='none'/>
</domain>
```



```shell
# Define the virtual machine
virsh define kvm1.xml

# List all instances in all states
virsh list --all
```



### Defining KVM instances by virt-inst

```shell
# installing the package:
sudo apt install virtinst

# define and start the new instance by invoking the virt-install
virt-install --name kvm2 --ram 1024 --disk path=/tmp/debian.img,format=raw --graphics vnc,listen=192.168.122.1 --noautoconsole --hvm --import

virsh list --all
 
# virtual machine definition file that was automatically generated
cat /etc/libvirt/qemu/kvm1.xml
```



### Starting, stopping, and removing KVM instances

```shell
# List all instances in all states
virsh list --all

virsh start kvm1

# Examine the running process for the virtual machine: 
pgrep -lfa qemu

# Terminate the VM and ensure its status changed from running to shut off: 
virsh destroy kvm1
virsh list --all

# Remove the instance definition: 
virsh undefine kvm1
virsh list --all
```



### Inspecting and editing KVM config

```shell
# Ensure that you have a running
virsh list

# Dump the instance configuration file to standard output (stdout).
virsh dumpxml kvm1

# Save the configuration to a new file, as follows: 
virsh dumpxml kvm1 > kvm1.xml

# Edit the configuration in place and change the available memory for the VM:
virsh edit kvm1
```



### Building new KVM instances with virt-install and using the console

```shell
# Install a new KVM virtual machine 
virt-install --name kvm3 --ram 1024 --extra args="text console=tty0 utf8 console=ttyS0,115200" --graphics vnc,listen=192.168.122.1 --hvm --location=http://ftp.us.debian.org/debian/dists/stable/main/installer-amd64/ --disk path=/tmp/kvm1.img,size=8

# Attach to the console
virsh console kvm3

# Start the newly provisioned VM
virsh start kvm1

# Using your favorite VNC client, connect to the instance
systemctl enable serial-getty@ttyS0.service
systemctl start serial-getty@ttyS0.service

# Close the VNC session and connect to the virtual instance from the host OS
virsh console kvm1
	free -m
	
Disconnect from the console using the Ctrl + ] key 

# Examine the image file created after the installation: 
qemu-img info /tmp/kvm1.img
```

