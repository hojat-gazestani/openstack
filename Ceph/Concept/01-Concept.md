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

+ Ceph Monitor

-  (ceph-mon) maintains maps of the cluster state
  - monitor map,
  - manager map,
  - OSD map,
  - MDS map,
  - CRUSH map.

+ Ceph Manager

+ Ceph Object Storage Daemons (OSDs)

```txt
 (for example, if three copies of a given object are stored in the Ceph cluster, then at least three OSDs must exist in that Ceph cluster).
```

+ Ceph Metadata Server

```txt
Necessary to run Ceph File System clients.
```
