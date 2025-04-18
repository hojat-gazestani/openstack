# Understanding Ceph components

- ODSs (Object-storage device node): 
	- Storage unit where data is kept.
	- daemon that interacts with the storage.
	- Thousands of os OSDs can exist in a cluster.
	
	- OSD daemon: made storage smart
		- Any block device with a file system that supports User Extended Attributes can be an OSD.
	- Every disk is an OSD and the number of OSDs is unlimited (24 hard drive = 24 OSDs)
	- OSD is the block device.
	- OSD daemon is the block device.
	
	- FAIL SCENARIO:
		1. Drive goes down -> OSD will goes down
		2. Monitor node will redistribute an update CRUSH map
		3. OSDs also respond to the update because redandancy is lost.
		4. My start to replicate non-redundant data to make it redundant again (across fewer nodes)

- MONs (Monitor node): 
	- Maintains a master copy of the storage cluster data map.
	- Provide access to OSDs.
	
	- Handle cluster quorum to avoid split brain situations, using the PAXOS algorithm.
		- Use one at least, 3-5 is recommended.
	- Keep tack of all existing MONs and OSDs.
	- Are the initial point of contact for Ceph clients.
		- Client upload to a primary OSD and the OSD calculates target OSDs for replicas, using the CRUSH algorithm
	
	- CRUSH: 
		- Controlled Replication Under Scalable Hashing.
		- It is a pseudo-random algorithm that ensure that identical objects will always end up on the same OSDs if the topology of the cluster has not changed.
		- Placement groups are used to write data to the OSDs.
		- Administrators can manipulate CRUSH to determine where objects are written.

- MDS  (Metadata server node): Stores all the filesystem metadata (directories, file ownership, access mode, and so on)
- Block device: rdb.
- Gateway: rgw; RESTful interface to Ceph.
- CephFS: file system

- Ceph pools: like a tenant in Openstack, is a user defined grouping of storage
	- Pools of storage is created wiht specific parameters, including resilience type, placement groups, CRUSH rules, ownership
	- Resilience type: Specifies how you want to data loss, along with the degree to which you're willing to ensure loass doesn't occcur.
					 - Two type of resilience are replication and erasure coding.
					 - The default resilience level for replication is two copies.
	- Placement group: Are defined aggregations of data objects used for tracking data accross OSDs.
					 - Simply put, this specifies the number of groups in which you want to place your data, across OSDs.
	- CRUSH ruls	  : These rules are used to determine where and how to place distributed data.
					 - Different rules exist based on the appropriateness of placement.
					 - For example, rules used in the placement of data across a single rack of hardware might not be optimal for a pool across geographic boundaries, so different rules could be used.
	- Ownership	   - : This define the owner of a particular pool through user ID.


# Understanding ODSs

- The starage backend (hard disk) is made smart by OSD daemons
	- Any block device with a file system that supports User Extended Attribute can be an OSD

- Every disk is an OSD and the number of OSDs is unlimited
- Note that the OSD is the block device, as well as the daemon that runs on top of it

# Understanding MONs

- MONs handls cluster quorum to avoid split brain situations, using the PAXOS algorithm.
	- Use on at least, 3-5 is recomended
- MONs keep track of all existing MONs and OSDs
- MONs are the initial point of contact for Ceph clients
	- Clients upload to a primary OSD and the OSD calculates target OSDs for replicas, using the CRUSH algorithm

# Understanding CURSH

- CRUSH is Controlled Replication Under Scalable Hashing
- It is a pseudo-random algorithm that nesures that identical objects will always end up on the same OSDs if the topology of the cluster has not changed.
- Placement groups are used to write data to the OSDs.
- Administrators can manipulate CRUSH to determine where objects are written.

# Authentication

- CephX is used as the authentication algorithm allowing users to access specific OSDs.
- Pools can be used to segregate the cluster into regions

# Know your MTU

- Ceph node communicate using the IP
- Small MTU 1500 bytes, create more small packet, leading to increased network overhead.
- Jumbo frame 9000 bytes, the payload could be transmitted in a single packet. 

# Design

- Network
	- public-facing network: carry client traffic
	- internal cluster network: carry heartbeat, replication and recovery traffic between OSDs

	- every write on the public network will cause (n-1) writes on the internal network, where n is the number of replicas.
	- Ceph will only acknowledge a write to the client when it has been written to the journal/WALs(write-ahead log) of all replicas
	- Avoid bottlenecked in replicated pools, consider sizing your cluster network to be n-1 times larger than the public network.

- More IOPS:
	- Ceph acknowledges a write to the client only once the data has been written to the write-ahead log (WAL) of the primary OSD and to the WALs of all replicas. 
	- So, faster WAl increase the IOPS.
	- WALs or BlueStore RocksDB metadata -> SSD at minimum, and NVMe if possible
	
	- If your HDD can write at 100MB/s sustained, and your SSD can manage 500MB/s sustained, 
	- more than one SSD/NVMe device per node for metadata/WAL to ensure that you won’t lose all OSDs on the node if a metadata device fails.

- Ceph redundancy (Rplication)
	- RAID-1 (replication)
	- RAID-5/6 (erasure encoding)
	- Imagine that instead of the array consisting of hard drives, it consist of entire servers.

	- With downside of storage cost: configure more than one replica instead of RAID-1
	- three-node cluster each node holds 33% of your data
	- ten node cluster, it’s only 10% per node

	- Forcing more network traffic across fewer nodes

- Erasure Encoding
	- With Ceph you are not confined to the limits of RAID-5/RAID-6 with just one or two 'redundant disks' (in Ceph's case storage nodes).
	- using "Erasure Encoding" you cal tell: "I want you to chop up my data in 8 data segments and 4 parity segments"- PIC-1
	- Can lose up to four entire hosts.
	- 33% storage overhead for redundancy instead of 50%
	- 8 + 4 = 12 storage nodes
	- you could do 6 data segments + 2 parity segments (similar to RAID-6) with only 8 hosts

- Ceph failure domains
	- CRUSH map can represent your physical datacenter topology, consisting of racks, rows, rooms, floors, datacenters
	- the cluster can tollerate failures across certain boundaries- PIC-2

- Bluestore performance Scalability ( 3 vs 5 nodes


- Consideration:
	- Should the replicated node be on the same rack or multiple racks to avoid SPOF ?
		- Suould the OSD traffic stay within the rack or span across rack in a dedicated or shared network ?
		- How many nodes failure can be tolerated ?
		- If the nodes are separated out across multiple racks network traffic increases and the impact of latency and the number of network switch hops should be considered.

	- Ceph will automatically recover by re-replicating data from the failed nodes using secondary copies present on other nodes in cluster . A node failure thus have several effects.

		- Total cluster capacity is reduced by some fractions.
		- Total cluster throughput is reduced by some fractions.
		- The cluster enters a write heavy recovery processes.

	- A general thumb of rule to calculate recovery time in a ceph cluster given 1 disk per OSD node is :

	- Recovery Time in seconds = disk capacity in Gigabits / ( network speed *(nodes-1) )

# Hardware

- Monitor nodes:
	- A minimum of three monitors nodes
	- 1U server with low cost processor E5-2603,16GB RAM and 1GbE network
	- if PG,Monitor and OSD logs are storage on local disk -> 
	
- Storage nodes:
	- POC Environment
	- minimum of 3 physical nodes with 10 OSD's each
	- 66% cluster availability upon a physical node failure and 97% uptime upon an OSD failure.
	- RGW and Monitor nodes can be put on OSD  nodes but this may impact performance  and not recommended for production.

	- Production Environment
	- minimum of 5 physically separated nodes and minimum of 100 OSD @ 4TB per OSD the cluster capacity is over 130TB
	- 80% uptime on physical node failure and 99% uptime on OSD failure
	- RGW and Monitors should be on separate nodes.

- Business Requirement
- Budget ?
- Do you need Ceph cluster for day to day operation or SPECIAL
- Technical Requirement
- What applications will be running on your ceph cluster ?
- What type of data will be stored on your ceph cluster 
- Should the ceph cluster be optimized for capacity and performance ?
- What should be usable storage capacity ?
- What is expected growth rate ?
- How many IOPS should the cluster support ?
- How much throughput should the cluster support
- How much data replication ( reliability level ) you need ?
	

[first]: https://google.com/

# Sources:

[cphe1]: https://ceph.io/en/news/blog/2014/zero-to-hero-guide-for-ceph-cluster-planning/
[ceph1]: https://ceph.io/community/part-3-rhcs-bluestore-performance-scalability-3-vs-5-nodes/
[medium]: https://medium.com/@adam.goossens/so-you-want-to-build-a-ceph-cluster-7ff9a033411d
[louwerntius]: https://louwrentius.com/understanding-ceph-open-source-scalable-storage.html

