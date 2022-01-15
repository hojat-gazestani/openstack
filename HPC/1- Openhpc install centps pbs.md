

### 5.2. Login to Linux machine 
```
ssh root@master.haii.or.th
```

5.3. Prepare before installation 
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

Install OpenHPC
---------------

### Install the OpenHPC repository
```
yum -y install http://build.openhpc.community/OpenHPC:/1.3/CentOS_7/x86_64/ohpcrelease-1.3-1.el7.x86_64.rpm
```

### Install OpenHPC Basic Package 
```
# yum -y install ohpc-base
# yum -y install ohpc-warewulf
‍‍‍‍‍‍‍```

### Set Time Server to time.haii.or.th
```
# systemctl enable ntpd.service
# echo "server time.haii.or.th" >> /etc/ntp.conf
# systemctl restart ntpd
```

### Install pb pro for Job Management 
```
# yum -y install pbspro-server-ohpc
```

### 5.8 Define internal interface, here use ens224
```
# perl -pi -e "s/device = eth1/device = enp0s3/" /etc/warewulf/provision.conf
```

### 5.9. Enable tftp service 
