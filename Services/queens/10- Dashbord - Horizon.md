## Dashbord - Horizon

```shell
sudo apt install openstack-dashboard
```


```shell
sudo vim  /etc/openstack-dashboard/local_settings.py
OPENSTACK_HOST = "controller"

ALLOWED_HOSTS = ['one.example.com', 'two.example.com']

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

CACHES = {
    'default': {
         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
         'LOCATION': 'controller:11211',
    }
}

OPENSTACK_KEYSTONE_URL = "http://%s:5000/v3" % OPENSTACK_HOST

OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = True

OPENSTACK_API_VERSIONS = {
    "identity": 3,
    "image": 2,
    "volume": 2,
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

TIME_ZONE = "TIME_ZONE"
````


```shell
sudo vim  /etc/apache2/conf-available/openstack-dashboard.conf
WSGIApplicationGroup %{GLOBAL}
````

### Finalize installation
```shell
sudo service apache2 reload
````

### Verify
```shell
http://controller/horizon
````