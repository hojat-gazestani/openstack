## Install and configure Placement from PyPI

### controller

```shell
sudo apt install python3-pip
sudo pip3 install python-openstackclient

sudo mysql

CREATE DATABASE placement;

GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'localhost' \
  IDENTIFIED BY 'openstack';
GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'%' \
  IDENTIFIED BY 'openstack';

. admin-openrc

openstack user create --domain default --password-prompt placement

openstack role add --project service --user placement admin

openstack service create --name placement \
  --description "Placement API" placement

openstack endpoint create --region RegionOne \
  placement public http://controller01:8778
openstack endpoint create --region RegionOne \
  placement internal http://controller01:8778
openstack endpoint create --region RegionOne \
  placement admin http://controller01:8778

pip3 install openstack-placement pymysql

sudo vim /etc/placement/placement.conf
[placement_database]
connection = mysql+pymysql://placement:openstack@controller01/placement

[api]
auth_strategy = keystone  

[keystone_authtoken]
www_authenticate_uri = http://controller01:5000/
auth_url = http://controller01:5000/
memcached_servers = controller01:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = placement
password = openstack

debug = true

$ sudo apt install python3-placement
$ placement-manage db sync
```

### Finalize installation 
```shell
sudo pip install uwsgi
sudo uwsgi -M --http :8778 --wsgi-file /usr/local/bin/ lacement-api \
        --processes 2 --threads 10

$ curl http://controller01:8778/
```