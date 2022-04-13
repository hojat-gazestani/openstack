## Keystone

```shell
sudo mysql

CREATE DATABASE keystone;

GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' \
IDENTIFIED BY 'xi6gileechi7Aem';
GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' \
IDENTIFIED BY 'xi6gileechi7Aem';


```shell
sudo apt install keystone  apache2 libapache2-mod-wsgi

sudo vim /etc/keystone/keystone.conf
[database]
connection = mysql+pymysql://keystone:xi6gileechi7Aem@TE-AZ-CN-01/keystone

[token]
provider = fernet
```

```shell
sudo su -s /bin/sh -c "keystone-manage db_sync" keystone

sudo  keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
sudo keystone-manage credential_setup --keystone-user keystone --keystone-group keystone


```
```shell
# keystone-manage bootstrap --bootstrap-password jihoo3gioChiHo4 \
  --bootstrap-admin-url http://TE-AZ-CN-01:5000/v3/ \
  --bootstrap-internal-url http://TE-AZ-CN-01:5000/v3/ \
  --bootstrap-public-url http://TE-AZ-CN-01:5000/v3/ \
  --bootstrap-region-id RegionOne

```

### Configure the Apache

```shell
sudo vim /etc/apache2/apache2.conf

ServerName TE-AZ-CN-01
```

### Finalize the installation

```shell
sudo service apache2 restart

export OS_USERNAME=admin
export OS_PASSWORD=
xport OS_PROJECT_NAME=admin
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_AUTH_URL=http://TE-AZ-CN-01:5000/v3
export OS_IDENTITY_API_VERSION=3

```

### Create a domain, projects, users, and roles

```shell
openstack domain create --description "An Example Domain" example

openstack project create --domain default \
  --description "Service Project" service

openstack project create --domain default \
  --description "Demo Project" demo

openstack user create --domain default \
  --password-prompt demo

openstack role create user

openstack role add --project demo --user demo user
```

### Verify operation

```shell
unset OS_AUTH_URL OS_PASSWORD

openstack --os-auth-url http://TE-AZ-CN-01:5000/v3 \
  --os-project-domain-name Default --os-user-domain-name Default \
  --os-project-name admin --os-username admin token issue

openstack --os-auth-url http://TE-AZ-CN-01:5000/v3 \
  --os-project-domain-name Default --os-user-domain-name Default \
  --os-project-name demo --os-username demo token issue
```

### Create OpenStack client environment scripts
```shell
vim admin-openrc
export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=ADMIN_PASS
export OS_AUTH_URL=http://TE-AZ-CN-01:5000/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2


vim demo-openrc
export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=demo
export OS_USERNAME=demo
export OS_PASSWORD=DEMO_PASS
export OS_AUTH_URL=http://TE-AZ-CN-01:5000/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2
```

### Using the scripts
```shell
. admin-openrc

openstack token issue
```