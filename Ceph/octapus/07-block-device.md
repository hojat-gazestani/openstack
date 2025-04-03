# Block device 

```sh
ceph osd pool create test-pool 
ceph osd pool ls detail

rdb pool init test-pool
ceph osd pool ls detail # Application rdb
ceph osd pool ls detail | grep application 

rdb create --size 10G --pool test-pool test-volume
rdb ls --pool test-pool -l
```

# Cephx
```sh
ceph auth ls
ceph auth add client.test mon 'allow r' osd 'allow rwx pool=test-pool'
cehp auth get client.test
# COPUY AUTH
ceph config generate-minimal-config     # cat /etc/ceph/ceph.config
# COPY CONFIG
```

# Client
```sh
CEPH_RELEASE=19.2.1
curl --silent --remote-name --location https://download.ceph.com/rpm-${CEPH_RELEASE}/el9/noarch/cephadm
chmod +x cephadm
sudo ./cephadm add-repo --release squid
apt update -y
apt install ceph-common -y
ceph -v
vim /etc/ceph/ceph.config
# PASTE CONFIG

vim /etc/ceph/ceph.keyring
# PASTE AUTH
```

```sh
lsmod | grep rdb
modprobe rdb

rdb -c /etc/ceph/ceph.config -k /etc/ceph/ceph.keyring -n client.test ls pool --pool test-pool -l 
rdb -n -n client.test device map --pool test-pool test-volume
# /dev/rdb0

sudo mkfs.ext4 /dev/rdb0
fdisk -l
mount /dev/rdb0 /mnt 
df -h
```
