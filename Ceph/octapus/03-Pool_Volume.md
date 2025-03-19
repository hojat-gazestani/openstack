# Pool, volume

- Creating pool
```sh
ceph -s

ceph osd pool create bdpooltest 64 # 64 placement group
ceph osd pool ls detail
# replication size 3
# pg_num 64
# pgp_num 64
# autoscalig_mode on

# initial pool as block device
rbd pool init bdpooltest
ceph osd pool ls detail
# application rbd
```

- Creating volume
```sh
# create volume
rbd create --size 10G --pool bdpooltest bdvolumetest
rbd ls --pool bdpooltest -l
rbd --pool bdpooltest rm bdvolumetest
```

```sh
ceph osd pool ls
ceph osd lspools
```

- Set pool quotas
```sh
ceph osd pool set-quota {pool-name} [max_objects {obj-count}]
ceph osd pool set-quota test-pool max_objects 1000

ceph osd pool ls detail | grep max_objects
```

- Delete a pool

```sh
ceph osd pool delete {pool-name} [{pool-name} --yes-i-really-really-mean-it]

ceph osd pool delete test-pool test-pool --yes-i-really-really-mean-it
ceph tell mon.\* injectargs '--mon-allow-pool-delete=true'
ceph osd pool delete test-pool test-pool --yes-i-really-really-mean-it
```

- Rename pool
```sh 
ceph osd pool rename test mypool
```

- Show pool statistics
```sh
rados df
```

- Get pool values
```sh
ceph osd pool get {pool-name} all
ceph osd pool get test-pool all
ceph osd pool get test-pool size
ceph osd pool get test-pool min_size
ceph osd pool get test-pool pgp_num
```

- Set the number of object replicas

```sh
ceph osd pool set {pool-name} size {num-replicas}
ceph osd pool set test-pool size 4
```