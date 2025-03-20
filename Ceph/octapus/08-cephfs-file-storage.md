# Ceph file storage

```sh
ceph -w
watch ceph orch ps
watch ceph osd pool ls
watch ceph orch ls
```

```sh
ceph fs volume create cephfs_a

ceph fs authorize cephfs_a client.foo / rw

ceph auth get client.foo
```


# Client side
```sh
apt install ceph-fuse ceph-common