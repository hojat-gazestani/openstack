# Ceph file storage New Version

```sh
ceph -w
watch ceph orch ps
watch ceph osd pool ls
watch ceph orch ls
```

```sh
ceph fs volume create cephfs-test

ceph fs authorize cephfs-test client.foo / rw
ceph fs authorize cephfs-test client.bar / r /dir1 rw

ceph auth get client.foo
```


# Client side
```sh
apt install ceph-fuse ceph-common ceph-fuse

vim /etc/ceph/client.key
# Paste key here

ceph-fuse --id foo /mnt/cephfs/test
```

# Impliment File storage CephFS Older version

## server side
```sh
ceph-deploy mds create {host1} {host2}
ceph-deploy mds create ceph-host1 ceph-host2

sudo systemctl start ceph-mds@ceph-host2
sudo systemctl enable ceph.target

ps -ef | grep mds
```

```sh
ceph mds stat

ceph osd pool create cephfs_data 128
ceph osd pool create cephfs_metadata 128
ceph osd pool ls

ceph fs new cephfs cephfs_metadata cephfs_data
ceph fs ls
ceph mds stat
ceph fs status

user@monitor# netstat -nap | grep 6789
```

## Client side

```sh
# Old version
su - cephadm
cd ceph_cluster
ceph-deploy install client1

# New version 
# Install ceph common


ceph --version

vim /etc/ceph/client.key
# Paste key here

vim /etc/ceph/ceph.conf
# Paste config here
mkdir -p /mnt/cephfs

mount -t ceph ceph-host1:6789:/ /mnt/cephfs -o name=admin,secretfile=ceph.key

ll /mnt/cephfs

df -h | grep /mnt
touch /mnt/cephfs/testfile
```

## Test
```sh
watch -d -n 1 "ceph osd tree"
wathh -d -n 1 "ceph -s"
client2# watch -d -n 1 "cat /mnt/cephfs/text.txt"
client1# echo test1 > /mnt/cephfs/test.txt

osd-node1# shutdown # or shutdown an OSD
```
