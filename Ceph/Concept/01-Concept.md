# Storage

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

### Block Storage

### File Storage

## Ceph Storage Cluster

### Ceph Monitor

-  (ceph-mon) maintains maps of the cluster state
  - monitor map,
  - manager map,
  - OSD map,
  - MDS map,
  - CRUSH map
  - Authentication between daemons and clients.


> Ceph stores data as objects within logical storage pools. Using the CRUSH algorithm, Ceph calculates which placement group (PG) should contain the object, and which OSD should store the placement group. The CRUSH algorithm enables the Ceph Storage Cluster to scale, rebalance, and recover dynamically.


### Ceph Manager

 > (ceph-mgr) is responsible for keeping track of runtime metrics and the current state of the Ceph cluster,

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

 > provides some monitoring information to Ceph Monitors and Managers by checking other Ceph OSD Daemons for a heartbeat.


### Ceph Metadata Server - ceph-mds

> Necessary to run Ceph File System clients.

> stores metadata on behalf of the Ceph File System (i.e., Ceph Block Devices and Ceph Object Storage do not use MDS). Ceph Metadata Servers allow POSIX file system users to execute basic commands (like ls, find, etc.) without placing an enormous burden on the Ceph Storage Cluster.
