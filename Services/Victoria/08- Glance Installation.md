## Glance Installation

### controller

```shell
sudo mysql

CREATE DATABASE glance;

GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' \
  IDENTIFIED BY 'openstack';
GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' \
  IDENTIFIED BY 'openstack';


. admin-openrc

openstack user create --domain default --password-prompt glance

openstack role add --project service --user glance admin

openstack service create --name glance \
  --description "OpenStack Image" image

openstack endpoint create --region RegionOne \
  image public http://controller2:9292
openstack endpoint create --region RegionOne \
  image internal http://controller2:9292
openstack endpoint create --region RegionOne \
  image admin http://controller2:9292

sudo apt install -y glance

sudo vim /etc/glance/glance-api.conf
[database]
connection = mysql+pymysql://glance:openstack@controller2/glance

[keystone_authtoken]
www_authenticate_uri = http://controller2:5000
auth_url = http://controller2:5000
memcached_servers = controller2:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = glance
password = openstack

[paste_deploy]
flavor = keystone

[glance_store]
stores = file,http
default_store = file
filesystem_store_datadir = /var/lib/glance/images/


sudo su -s /bin/sh -c "glance-manage db_sync" glance

sudo service glance-api restart
```