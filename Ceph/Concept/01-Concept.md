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

## Replica

- pool size 3 with create 3 copy of data or 3 replication

![replica](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/Concept/Pic/replica.png)

## eracure


# Network

- Ceph Clients make requests directly to Ceph OSD Daemons. Ceph OSD Daemons perform data replication on behalf of Ceph Clients, which means replication and other factors impose additional loads on Ceph Storage Cluster networks.

- **Public network** : client, front-side

- **Cluster network**: private, replication, back-side

[source](https://docs.ceph.com/en/reef/rados/configuration/network-config-ref/)

![netowrk](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/Concept/Pic/network.png)
