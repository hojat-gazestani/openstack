## placement group

```txt
pool: Logical volume, placement group

Note: each PG can assign to one pool
pool1: PG1, PG2, PG3, PG4
pool2: PG5, PG6, PG7, PG9

Placement group map:
	specify which object location for specific user - scailable

pool -> pg :
			pg_num 		32, 64, 128
			pgp_num		auto scailing

Search: setting the number of pgs ceph
```

- PG
```sh
ceph pg stat
ceph pg dump
ceph pg dump pgs
ceph pg dump osds
ceph pg dump pools

ceph pg dump -o /opt/pg --format=json
```