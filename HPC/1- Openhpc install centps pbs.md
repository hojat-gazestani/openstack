OpenHPC Install CentOS
======================


### 5.2. Login to Linux machine 
```
ssh root@master.haii.or.th
```

## 5.3. Prepare before installation 
--------------------------------

### add hosts file 
```
# vi /etc/hosts
192.168.1.254 master
```

### Turn off Firewall 
```
# systemctl disable firewalld
# systemctl stop firewalld
```

### Update the system
```
# yum -y update
# yum -y install wget
```

## 5.4 Install the OpenHPC repository
```
# yum -y install http://build.openhpc.community/OpenHPC:/1.3/CentOS_7/x86_64/ohpcrelease-1.3-1.el7.x86_64.rpm
```

## 5.5 Install OpenHPC Basic Package 
```
# yum -y install ohpc-base
# yum -y install ohpc-warewulf
```

## 5.6 Set Time Server to time.haii.or.th
```
# systemctl enable ntpd.service
# echo "server time.haii.or.th" >> /etc/ntp.conf
# systemctl restart ntpd
```

## 5.7 Install pb pro for Job Management 
```
# yum -y install pbspro-server-ohpc
```

## 5.8 Define internal interface, here use ens224
```
# perl -pi -e "s/device = eth1/device = enp0s3/" /etc/warewulf/provision.conf
```

## 5.9. Enable tftp service 
```
# perl -pi -e "s/^\s+disable\s+= yes/ disable = no/" /etc/xinetd.d/tftp
```

## 5.10 Assign ip to ens224
```
# ifconfig ens224 192.168.1.254 netmask 255.255.255.0 up
```

## 5.11 Restart the service in use. 
```
# systemctl restart xinetd
# systemctl enable mariadb.service
# systemctl restart mariadb
# systemctl enable httpd.service
# systemctl restart httpd
# systemctl enable dhcpd.service
```

## 5.12 Set the image for the compute node here as 
```
# export CHROOT=/opt/ohpc/admin/images/centos7.4
# wwmkchroot centos-7 $CHROOT
```

## 5.13 Install OpenHPC for compute node 
```
# yum -y --installroot=$CHROOT install ohpc-base-compute
```

## 5.14 Edit the resolv.conf file for the compute node. 
```
# cp -p /etc/resolv.conf $CHROOT/etc/resolv.conf
```

## 5.15. Install pbspro for compute node 

### set PBS_SERVER=master, clienthost master 
```
# yum -y --installroot=$CHROOT install pbspro-execution-ohpc
# perl -pi -e "s/PBS_SERVER=\S+/PBS_SERVER=master/" $CHROOT/etc/pbs.conf
# perl -pi -e "s/\$clienthost \S+/\$clienthost master/" $CHROOT/var/spool/pbs/mom_priv/config
# chroot $CHROOT opt/pbs/libexec/pbs_habitat
# echo "\$usecp *:/home /home" >> $CHROOT/var/spool/pbs/mom_priv/config
# chroot $CHROOT systemctl enable pbs
```

## 5.16. Install NTP for compute node 
```
# yum -y --installroot=$CHROOT install ntp
```

## 5.17. Install kernel for compute node 
```
# yum -y --installroot=$CHROOT install kernel
```

## 5.18. Install modules user environment for compute node 
```
# yum -y --installroot=$CHROOT install lmod-ohpc
```

## 5.19. Create OpenHPC Defaults 
```
# wwinit database
# wwinit ssh_keys
```

## 20. Create an NFS Client 
It mounts /home and /opt/ohpc/pub from 192.168.1.254(master).
```
# echo "192.168.1.254:/home /home nfs nfsvers=3,nodev,nosuid,noatime 0 0" >> $CHROOT/etc/fstab
# echo "192.168.1.254:/opt/ohpc/pub /opt/ohpc/pub nfs nfsvers=3,nodev,noatime 0 0" >> $CHROOT/etc/fstab
```

