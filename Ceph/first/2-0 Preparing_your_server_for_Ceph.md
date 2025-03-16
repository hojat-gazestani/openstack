# Required Servers

- You'll need 4 servers
	1. 1 Ceph admin node (admin)
	2. 3 Ceph storage nodes (node1, node2, node3)
		- One dedicated disk (10G suggested) available on each
	3. 1 client node using the RADOS Block device (client0)
	4. 2 optional gateway node for running the ceph-radosgw service (gateway)

# Preparing Servers to run Ceph

- An admin node is set up to use ceph-deploy; from the admin node the configuration is pushed to the participating nodes.
- All nodes need to be stup for passwordless login through sudo for a specific Ceph user
- Time synchronization is mandatory
- Port 6789/tcp must be open in the firewall

# Ceph Installation method

```txt
cephadm:        Octopus and newer releases.
ceph-deploy:    Nautilus and older release.
Rook:           Nautilus and newer releases of Ceph.
                manages Ceph clusters running in Kubernetes,
ceph-ansible:   introduced in Nautlius and Octopus,
                is not integrated with the new orchestrator APIs
```