## Block Storage
```shell

sudo apt install lvm2 thin-provisioning-tools

sudo pvcreate /dev/sdb
sudo vgcreate cinder-volumes /dev/sdb

sudo vim /etc/lvm/lvm.conf
devices {
filter = [ "a/sda/", "a/sdb/", "r/.*/"]

sudo apt install cinder-volume

sudo vim /etc/cinder/cinder.conf
[DEFAULT]
auth_strategy = keystone
transport_url = rabbit://openstack:openstack@controller01
enabled_backends = lvm
glance_api_servers = http://controller01:9292

[database]
connection = mysql+pymysql://cinder:openstack@controller01/cinder

[keystone_authtoken]
www_authenticate_uri = http://controller01:5000
auth_url = http://controller01:5000
memcached_servers = controller01:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = cinder
password = openstack

[lvm]
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
volume_group = cinder-volumes
target_protocol = iscsi
target_helper = tgtadm

[oslo_concurrency]
lock_path = /var/lib/cinder/tmp

```
### controller 
```shell

. admin-openrc
openstack volume service list


sudo service tgt restart
sudo service cinder-volume restart

```
### Block storage 
```shell
. demo-openrc

openstack volume create --size 1 volume1

openstack volume list

openstack server add volume INSTANCE_NAME VOLUME_NAME
openstack server add volume provider-instance volume1

openstack volume list

ssh provider-instance
sudo fdisk -l
```