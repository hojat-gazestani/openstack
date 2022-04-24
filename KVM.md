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
virt-install --name kvm2 --ram 1024 --disk path=debian.img,format=raw --graphics vnc,listen=192.168.122.1 --extra-args='console=tty0' -v --hvm --import

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

# error: Refusing to undefine while domain managed save image exists
virsh managedsave-remove kvm1
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
virt-install --name kvm22 --ram 1024 --extra args="text console=tty0 utf8 console=ttyS0,115200" --graphics vnc,listen=192.168.122.1 --hvm --location=http://ftp.ir.debian.org/debian/dists/stable/main/installer-amd64/ --disk path=kvm22.img,size=8

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



### Create A KVM Virtual Machine Using Qcow2 Image

```shell
virt-customize -a debian-9.qcow2 --root-password password:123

virt-install --name debian9 --memory 2048 --vcpus 1 --disk ./debian-9.qcow2,bus=sata --import --os-variant debian9 --network default --vnc --noautoconsole 


# List OS Variants
osinfo-query os

# To launch the same VM next time, run:
virsh --connect qemu:///system start centos8
```



### Managing CPU and memory resources in KVM

```shell
# Get memory statistics for the running instance:
virsh dommemstat kvm1

# To increase the maximum amount of memory that can be allocated to the VM
virsh setmaxmem kvm1 4G --config
virsh setmaxmem kvm1 512M --config

# Update the available memory for the VM to 2 GB
virsh setmem kvm1 --size 512M

virsh dumpxml kvm1 | grep memory

####
# CPUs:
####

# Get information about the guest CPUs: 
virsh vcpuinfo kvm1

# List the number of virtual CPUs used by the guest OS: 
virsh vcpucount kvm1

# Change the number of allocated CPUs to 4 for the VM
virsh edit kvm1
 
# Ensure that the CPU count update took effect: 
virsh vcpucount kvm1
virsh dumpxml kvm1 | grep -i cpu
```



### Attaching block devices to virtual machines

```shell
# Create a new 1 GB image file:
dd if=/dev/zero of=/tmp/new_disk.img bs=1M count=1024

# Attach the file as a new disk to the KVM instance: 
virsh attach-disk kvm1 /tmp/new_disk.img vda --live

# Connect to the KVM instance via the console: 
virsh console kvm1
	# Print the kernel ring buffer and check for the new block device: 
	dmesg | grep vda

	# Examine the new block device: 
	fdisk -l /dev/vda

# Dump the instance configuration from the host OS: 
virsh dumpxml kvm1

# Get information about the new disk: 
virsh domblkstat kvm1 vda

# Detach the disk: 
virsh detach-disk kvm1 vda --live

# Copy or create a new raw image: 
cp /tmp/new_disk.img /tmp/other_disk.img

# Write the following config file: 
cat other_disk.xml

# Attach the new device: 
virsh attach-device kvm1 --live other_disk.xml

# Detach the block device: 
 virsh detach-device kvm1 other_disk.xml --live
```



### Sharing dirctory between a running VM and host OS

```shell
mkdir /tmp/shared
touch /tmp/shared/file

virsh edit kvm1
<devices>
    ...
    <filesystem type='mount' accessmode='passthrough'>
    <source dir='/home/hoji/Documents/ww/kvm/shared'/>
    <target dir='tmp_shared'/>
    </filesystem>
    ...fie
</devices>

# Selinux configuration
sudo semanage fcontext -a -t svirt_image_t "/home/hoji/Documents/ww/kvm/shared(/.*)?"
sudo restorecon -vR /home/hoji/Documents/ww/kvm/shared

virsh start kvm1

virsh console kvm1
	lsmod | grep 9p
	mount -t 9p -o trans=virtio tmp_shared /mnt
	mount | grep tmp_shared
	ls -la /mnt/
```



### Autostarting KVM instances

```shell
# Enable the VM autostart: 
virsh autostart kvm1

# Obtain information for the instance: 
virsh dominfo kvm1

# Stop the running instance and ensure that it is in the shut off state: 
virsh destroy kvm1
virsh list --all

# Stop the libvirt daemon and ensure that it is not running: 
/etc/init.d/libvirt-bin stop
pgrep -lfa libvirtd

# Start back the libvirt daemon:
/etc/init.d/libvirt-bin start

# List all running instances: 
virsh list --all

# Disable the autostart option: 
virsh autostart kvm1 --disable

# Verify the change: 
virsh dominfo kvm1 | grep -i autostart
 
```



### Working with storage pools

```shell
# Copy the raw Debian image file 
cp /tmp/kvm1.img /var/lib/libvirt/images/

# Create the following storage pool definition: 
cat file_storage_pool.xml
<pool type="dir">
  <name>file_virtimages</name>
  <target>
    <path>/var/lib/libvirt/images</path>
  </target>
</pool>

# Cannot access storage file, Permission denied Error in KVM Libvirt
sudo vim /etc/libvirt/qemu.conf
	user = "hoji"
	group = "libvirt"

sudo systemctl restart libvirtd
sudo usermod -a -G libvirt $(whoami)
sudo chown hoji:libvirt /var/lib/libvirt/images

# Define the new storage pool
virsh pool-define file_storage_pool.xml

# List all storage pools: 
virsh pool-list --all

# Start the new storage pool and ensure that it's active: 
virsh pool-start file_virtimages
virsh pool-list --all

# Enable the autostart feature on the storage pool: 
virsh pool-autostart file_virtimages
virsh pool-list --all
 
# Obtain more information about the storage pool: 
virsh pool-info file_virtimages

# List all volumes that are a part of the storage pool: 
virsh vol-list file_virtimages

# Obtain information on the volume:
virsh vol-info /var/lib/libvirt/images/kvm1.img

# Start new KVM instance using the storage pool and volume
virt-install --name kvm1 --ram 1024 --graphics vnc,listen=146.20.141.158 --hvm --disk vol=file_virtimages/kvm1.img --import

virsh list --all
```



### Managing volumes

```shell
# List the available storage pools: 
virsh pool-list --all

# List the available volumes, that are a part of the storage pool:
virsh vol-list file_virtimages

# Create a new volume with the specified size:
virsh vol-create-as file_virtimages new_volume.img 9G

# List the volumes on the filesystem: 
ls -lah /var/lib/libvirt/images/
 
# Obtain information about the new volume: 
qemu-img info /var/lib/libvirt/images/new_volume.img
 
# Use the virsh command to get even more information:
virsh vol-info new_volume.img --pool file_virtimages

# Dump the volume configuration: 
virsh vol-dumpxml new_volume.img --pool file_virtimages
 
# Resize the volume and display the new size: 
virsh vol-resize new_volume.img 10G --pool file_virtimages
virsh vol-info new_volume.img --pool file_virtimages

# Delete the volume and list all available volumes in the storage pool: 
virsh vol-delete new_volume.img --pool file_virtimages
virsh vol-list file_virtimages

# Clone the existing volume: 
virsh vol-clone kvm1.img kvm2.img --pool file_virtimages
virsh vol-list file_virtimages


```



### Managing secrets

```shell
# List all available secrets:
virsh secret-list
```



```html
# Create the following secrets definition:
vim volume_secret.xml
<secret ephemeral='no'>
  <description>Passphrase for the iSCSI iscsi-target.linux-admins.net target server</description> 	   <usage type='iscsi'>
    <target>iscsi_secret</target>
  </usage>
</secret>
```



```shell
# Create the secret and ensure that it has been successfully created:
virsh secret-define volume_secret.xml
virsh secret-list

# Set a value for the secret:
virsh secret-set-value 7ad1c208c2c5-4723-8dc5-e2f4f576101a $(echo "some_password" | base64)
```



```html
# Create a new iSCSI pool definition file:
vim iscsi.xml
<pool type='iscsi'>
  <name>iscsi_virtimages</name>
  <source>
    <host name='iscsi-target.linux-admins.net'/>
    <device path='iqn2004-04.ubuntu:ubuntu16:iscsi.libvirtkvm'/>
    <auth type='chap' username='iscsi_user'>
      <secret usage='iscsi_secret'/>
    </auth>
  </source>
  <target>
    <path>/dev/disk/by-path</path>
  </target>
</pool>

```



## KVM Networking with libvirt

