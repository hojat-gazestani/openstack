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

