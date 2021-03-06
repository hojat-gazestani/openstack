##  horizon installation for Victoria
```shell

sudo apt install openstack-dashboard -y

sudo vim /etc/openstack-dashboard/local_settings.py
OPENSTACK_HOST = "controller01"
ALLOWED_HOSTS = ['*']

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

CACHES = {
    'default': {
         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
         'LOCATION': 'controller01:11211',
    }
}

OPENSTACK_KEYSTONE_URL = "http://%s/identity/v3" % OPENSTACK_HOST

OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = True

OPENSTACK_API_VERSIONS = {
    "identity": 3,
    "image": 2,
    "volume": 3,
}

OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = "Default"

OPENSTACK_KEYSTONE_DEFAULT_ROLE = "user"

OPENSTACK_NEUTRON_NETWORK = {
    ...
    'enable_router': False,
    'enable_quotas': False,
    'enable_ipv6': False,
    'enable_distributed_router': False,
    'enable_ha_router': False,
    'enable_lb': False,
    'enable_firewall': False,
    'enable_vpn': False,
    'enable_fip_topology_check': False,
}

TIME_ZONE = "Asia/Tehran"

sudo vim /etc/apache2/conf-available/openstack-dashboard.conf
WSGIApplicationGroup %{GLOBAL}

```
### Finalize installation 
```shell
sudo systemctl reload apache2.service
```
### Verify operation for Ubuntu
```shell
http://controller01/horizon
```
