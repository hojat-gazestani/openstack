### ODL Installation - Contrller Node
```shell

openstack router remove subnet router1 subnet1ID
openstack router delete router1

Object=("server" "subnet" "router"  "port"  "network")
for Obj in "${Object[@]}"; do
    for HashID in `openstack $Obj list -c ID | head -n -1 | tail -n +4 | cut -d ' ' -f 2`; do
        openstack $Obj delete $HashID
    done
done

sudo systemctl stop neutron-server openvswitch-switch
sudo apt purge neutron-openvswitch-agent -y     # OpenDaylight will be controlling the nodes, Delete it on every nodes

sudo rm -rf /var/log/openvswitch/*
sudo rm -rf /etc/openvswitch/conf.db

sudo service openvswitch-switch start
sudo ovs-vsctl show #This command must return the empty set except OpenVswitch

sudo pip install networking_odl

sudo vim /etc/neutron/neutron.conf
[DEFAULT]
core_plugin = neutron.plugins.ml2.plugin.Ml2Plugin
service_plugins = odl-router_v2

[qos]
notification_drivers = odl-qos

#        /etc/neutron/plugins/ml2/ml2_conf_odl.ini
sudo vim /etc/neutron/plugins/ml2/ml2_conf.ini
[ml2]
mechanism_drivers = opendaylight_v2
type_drivers = local,flat,vlan,vxlan
tenant_network_types = vxlan
extension_drivers = port_security, qos

[ml2_type_vxlan]
vni_ranges = 1:1000

[ml2_type_vlan]
network_vlan_ranges = PHYSICAL_NETWORK:MIN_VLAN_ID:MAX_VLAN_ID
network_vlan_ranges = physnet1,physnet2:1001:2000

[securitygroup]
enable_security_group = true

[ml2_odl]
username = <ODL_USERNAME>
password = <ODL_PASSWORD>
url = http://controller01:8080/controller/nb/v2/neutron
port_binding_controller = pseudo-agentdb-binding
enable_dhcp_service = True

Compute/network
===============
sudo apt install openvswitch-switch
sudo systemctl start openvswitch-switch.service
/usr/share/openvswitch/scripts/ovs-ctl start

sudo ovs-vsctl show
#Open vSwitch ID

sudo ovs-vsctl set Open_vSwitch <OPENVSWITCH ID> other_config={local_ip=<TUNNEL INTERFACE IP>}
sudo ovs-vsctl set-manager tcp:<OPENDAYLIGHT MANAGEMENT IP>:6640

sudo ovs-vsctl set-manager tcp:${ODL_IP_ADDRESS}:6640

sudo ovs-vsctl add-br br-ex
sudo ovs-vsctl add-port br-ex <INTERFACE NAME OF EXTERNAL NETWORK> #commonly eth0 or p2p1
sudo ovs-vsctl show

sudo neutron-odl-ovs-hostconfig
sudo ovs-vsctl show

```
### Verifying the inegration
````shell

neutron router-create router1
neutron net-create private
neutron subnet-create private --name=private_subnet 172.0.0.0/24
neutron router-interface-add router1 private_subnet
nova boot --flavor <flavor> --image <image id> --nic net-id=<network id> vinoth-vm1

curl -u admin:admin http://${OPENDAYLIGHTs SERVER}:8080/controller/nb/v2/neutron/networks

````
### sources
```shell
https://superuser.openstack.org/articles/open-daylight-integration-with-openstack-a-tutorial/
https://docs.openstack.org/networking-odl/pike/install/installation.html
https://docs.opendaylight.org/projects/netvirt/en/latest/openstack-guide/openstack-with-netvirt.html
http://sapham.net/2019/05/18/opendaylight-101-integrate-with-openstack.html

```