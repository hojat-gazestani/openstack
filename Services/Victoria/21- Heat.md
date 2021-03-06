## Heat installation

### controller
```shell

sudo mysql

GRANT ALL PRIVILEGES ON heat.* TO 'heat'@'localhost' \
  IDENTIFIED BY 'openstack';
GRANT ALL PRIVILEGES ON heat.* TO 'heat'@'%' \
  IDENTIFIED BY 'openstack';

. admin-openrc

openstack user create --domain default --password-prompt heat

openstack role add --project service --user heat admin

openstack service create --name heat \
  --description "Orchestration" orchestration
openstack service create --name heat-cfn \
  --description "Orchestration"  cloudformation

openstack endpoint create --region RegionOne \
  orchestration public http://controller01:8004/v1/%\(tenant_id\)s
openstack endpoint create --region RegionOne \
  orchestration internal http://controller01:8004/v1/%\(tenant_id\)s
openstack endpoint create --region RegionOne \
  orchestration admin http://controller01:8004/v1/%\(tenant_id\)s

openstack endpoint create --region RegionOne \
  cloudformation public http://controller01:8000/v1
openstack endpoint create --region RegionOne \
  cloudformation internal http://controller01:8000/v1
openstack endpoint create --region RegionOne \
  cloudformation admin http://controller01:8000/v1

openstack domain create --description "Stack projects and users" heat
openstack user create --domain heat --password-prompt heat_domain_admin
openstack role add --domain heat --user-domain heat --user heat_domain_admin admin
openstack role create heat_stack_owner
openstack role add --project demo --user demo heat_stack_owner
openstack role create heat_stack_user

sudo apt-get install heat-api heat-api-cfn heat-engine

sudo vim /etc/heat/heat.conf
[DEFAULT]
transport_url = rabbit://openstack:openstack@controller01
heat_metadata_server_url = http://controller01:8000
heat_waitcondition_server_url = http://controller01:8000/v1/waitcondition

stack_domain_admin = heat_domain_admin
stack_domain_admin_password = openstack
stack_user_domain_name = heat

[database]
connection = mysql+pymysql://heat:openstack@controller01/heat

[keystone_authtoken]
www_authenticate_uri = http://controller01:5000
auth_url = http://controller01:5000
memcached_servers = controller01:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = heat
password = openstack

[trustee]
auth_type = password
auth_url = http://controller01:5000
username = heat
password = openstack
user_domain_name = default

[clients_keystone]
auth_uri = http://controller01:5000

sudo su -s /bin/sh -c "heat-manage db_sync" heat

# service heat-api restart
# service heat-api-cfn restart
# service heat-engine restart

source:
https://docs.openstack.org/heat/victoria/install/
```