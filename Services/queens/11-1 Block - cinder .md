## Block - Cinder

```shell
sudo apt install lvm2 thin-provisioning-tools
```

```shell
sudo pvcreate /dev/sdb
sudo vgcreate cinder-volumes /dev/sdb
````

```shell
sudo vim /etc/lvm/lvm.conf
devices {
...
filter = [ "a/sdb/", "r/.*/"]
filter = [ "a/sda/", "a/sdb/", "r/.*/"]
filter = [ "a/sda/", "r/.*/"]
````

### Install and configure components
```shell
sudo apt install cinder-volume
````

```shell
sudo vim /etc/cinder/cinder.conf
[database]
# ...
connection = mysql+pymysql://cinder:CINDER_DBPASS@controller/cinder

[DEFAULT]
# ...
transport_url = rabbit://openstack:RABBIT_PASS@controller
auth_strategy = keystone
my_ip = MANAGEMENT_INTERFACE_IP_ADDRESS
enabled_backends = lvm
glance_api_servers = http://controller:9292

[keystone_authtoken]
# ...
auth_uri = http://controller:5000
auth_url = http://controller:5000
memcached_servers = controller:11211
auth_type = password
project_domain_id = default
user_domain_id = default
project_name = service
username = cinder
password = CINDER_PASS

[lvm]
# ...
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
volume_group = cinder-volumes
iscsi_protocol = iscsi
iscsi_helper = tgtadm

[oslo_concurrency]
# ...
lock_path = /var/lib/cinder/tmp
````

### Finalize installation
```shell
sudo service tgt restart
sudo service cinder-volume restart
````