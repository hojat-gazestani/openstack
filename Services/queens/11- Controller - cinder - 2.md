## controller - cinder

```shell
sudo mysql

CREATE DATABASE cinder;

GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'localhost' \
  IDENTIFIED BY 'CINDER_DBPASS';
RANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'%' \
  IDENTIFIED BY 'CINDER_DBPASS';


```

```shell
. admin-openrc

openstack user create --domain default --password-prompt cinder

openstack role add --project service --user cinder admin

openstack service create --name cinderv2 \
  --description "OpenStack Block Storage" volumev2

openstack service create --name cinderv3 \
  --description "OpenStack Block Storage" volumev3

openstack endpoint create --region RegionOne \
  volumev2 public http://controller:8776/v2/%\(project_id\)s
openstack endpoint create --region RegionOne \
  volumev2 internal http://controller:8776/v2/%\(project_id\)s
openstack endpoint create --region RegionOne \
  volumev2 admin http://controller:8776/v2/%\(project_id\)s

openstack endpoint create --region RegionOne \
  volumev3 public http://controller:8776/v3/%\(project_id\)s
openstack endpoint create --region RegionOne \
  volumev3 internal http://controller:8776/v3/%\(project_id\)s
openstack endpoint create --region RegionOne \
  volumev3 admin http://controller:8776/v3/%\(project_id\)s




````

### Install and configure components

```shell
sudo apt install cinder-api cinder-scheduler

sudo vim /etc/cinder/cinder.conf 
[database]
# ...
connection = mysql+pymysql://cinder:CINDER_DBPASS@controller/cinder

[DEFAULT]
# ...
transport_url = rabbit://openstack:RABBIT_PASS@controller
auth_strategy = keystone
my_ip = 10.0.0.11

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

[oslo_concurrency]
# ...
lock_path = /var/lib/cinder/tmp

```

```shell
sudo  su -s /bin/sh -c "cinder-manage db sync" cinder
````

### Configure Compute to use Block Storage

```shell
sudo vim /etc/nova/nova.conf
[cinder]
os_region_name = RegionOne
````

### Finalize installation

```shell
sudo service nova-api restart

sudo service cinder-scheduler restart
sudo service apache2 restart
````