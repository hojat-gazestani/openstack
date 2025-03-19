# Storage

## RADOS

![rados](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/Concept/Pic/01-rados.png)

```text
RADOS is an object storage system layer that provides a data durability and availability framework that all user-facing Ceph services are layered atop. RADOS is:

Highly available with no single point of failure (SPoF)
Reliable and resilient
Self-healing
Self-managing
Adaptive
Scalable
Not found on the Galactica

RADOS manages the distribution of data within Ceph. Durability and availability of data are adaptively maintained by initiating operations as needed to recover
```

## Ceph feature

+ Vertical Scaling vs Horizontal Scaling

+ Redundant array of independent disks (RAID)  

+ Availability

+ Security

+ Scalability

+ Sharing resources - Storage

+ Performance

+ Peer to Peer

# Storing data

- Recived data will be stored as RADOS objects in OSDs.

![objects](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/Concept/Pic/ceph-objects.png)

- Ceph OSD Daemons store data as objects in a flat namespace.
- An object has an identifier, binary data, and metadata consisting of name/value pairs.
- For example, CephFS uses metadata to store file attributes such as the file owner, the created date, and the last modified date.

![binary](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/Concept/Pic/binary.png)

## Type of Storages

### Object Storage
```txt
RestAPI
POST, PUT, GET

```

### Block Storage
```txt
dev/sda mount(Library) on OS
ext4
ntfs
```

### File Storage

```txt
SMB, file Sharing
```
## Ceph Storage Cluster

### Ceph Monitor

-  (ceph-mon) maintains maps of the cluster state (cluster map)
  - monitor map,
  - manager map,
  - OSD map,
  - MDS map,
  - CRUSH map
  - Authentication between daemons and clients.


> Ceph stores data as objects within logical storage pools. Using the CRUSH algorithm, Ceph calculates which placement group (PG) should contain the object, and which OSD should store the placement group. The CRUSH algorithm enables the Ceph Storage Cluster to scale, rebalance, and recover dynamically.


### Ceph Manager

 > (ceph-mgr) is responsible for keeping track of runtime metrics and the current state of the Ceph cluster,
 > endpoint for monitoring, orchestration, and plug-in modules.

 - storage utilization,
 - current performance metrics,
 - system load

 > storage utilization, current performance metrics, and system load

 - web-based Ceph Dashboard
 - REST API.

### Ceph Object Storage Daemons (OSDs) ceph-osd


 > (for example, if three copies of a given object are stored in the Ceph cluster, then at least three OSDs must exist in that Ceph cluster).

 - stores data,
 - handles data replication,
 - recovery,
 - rebalancing,
 - provides some monitoring information

 > checks its own state and the state of other OSDs and reports back to monitors.
 > provides some monitoring information to Ceph Monitors and Managers by checking other Ceph OSD Daemons for a heartbeat.


### Ceph Metadata Server - ceph-mds

> Necessary to run Ceph File System clients.
> manages file metadata when CephFS is used to provide file services.

> stores metadata on behalf of the Ceph File System (i.e., Ceph Block Devices and Ceph Object Storage do not use MDS). Ceph Metadata Servers allow POSIX file system users to execute basic commands (like ls, find, etc.) without placing an enormous burden on the Ceph Storage Cluster.

# Ceph clients

## librados

- Using `librdos` native protocol client directly interact with Ceph

![librados](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/Concept/Pic/librados.png)


# Pool

- Pools in logical partition distributed over OSDs

![pool](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/Concept/Pic/Pools.png)
 
- Ceph Clients retrieve a Cluster Map from a Ceph Monitor, and write RADOS objects to pools. The way that Ceph places the data in the pools is determined by the pool’s size or number of replicas, the CRUSH rule, and the number of placement groups in the pool

![map](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/Concept/Pic/cluster-map.png)

- PGs in a pool are related to different OSDs

![pool-pg](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/Concept/Pic/Pools.png)

## Replica

- pool size 3 with create 3 copy of data or 3 replication

![replica](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/Concept/Pic/replica.png)

## eracure


# Placement group

## Mapping PGs to OSDs

- Each Pool has number of PGs within it.
- CRUSH dynamically maps PGs to OSDs
- The dynamic approach provide a abstraction and indirection layer between Ceph OSD Daemons and Ceph Clients
- If the Ceph Client “knew” which Ceph OSD Daemons were storing which objects, a tight coupling would exist between the Ceph Client and the Ceph OSD Daemon

![PG-to-OSD](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/Concept/Pic/PlacementGrouop.png)

## rebalancing

- When you add a Ceph OSD Daemon to a Ceph Storage Cluster, the cluster map gets updated with the new OSD


# Network

- Ceph Clients make requests directly to Ceph OSD Daemons. Ceph OSD Daemons perform data replication on behalf of Ceph Clients, which means replication and other factors impose additional loads on Ceph Storage Cluster networks.

- **Public network** : client, front-side

- **Cluster network**: private, replication, back-side

[source](https://docs.ceph.com/en/reef/rados/configuration/network-config-ref/)

![netowrk](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/Concept/Pic/network.png)


# Authentication with cephx

- cephx uses shared secret keys for authentication, meaning both the client and Ceph Monitors have a copy of the client’s secret key. 
- the `client.admin` user invokes `ceph auth get-or-create-key` from the command line to generate a user name and secret key

![cephx-key](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/Concept/Pic/cephx-key.png)

- After creating a ticket on a session, The client decrypts the ticket and uses it to sign requests to OSDs and metadata servers throughout the cluster. 

![cephx-ticket](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/Concept/Pic/cephx-ticket.png)

- Each message sent between a client and a server after the initial authentication is signed using a ticket that the monitors, OSDs, and metadata servers can verify with their shared secret. 

![cephx-req-res](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/Concept/Pic/cephx-req-res.png)