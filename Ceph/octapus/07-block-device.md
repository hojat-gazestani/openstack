# Block device 

```sh
ceph osd pool create test-pool 
ceph osd pool ls detail

rbd pool init test-pool
ceph osd pool ls detail # Application rbd
ceph osd pool ls detail | grep application 

rbd create --size 10G --pool test-pool test-volume
rbd ls --pool test-pool -l
```

# Cephx
```sh
ceph auth ls
ceph auth add client.test mon 'allow r' osd 'allow rwx pool=test-pool'
ceph auth get client.test
# COPUY AUTH
ceph config generate-minimal-conf     # cat /etc/ceph/ceph.config
# COPY CONFIG
```

# Client
```sh
CEPH_RELEASE=19.2.1
curl --silent --remote-name --location https://download.ceph.com/rpm-${CEPH_RELEASE}/el9/noarch/cephadm
chmod +x cephadm
sudo ./cephadm add-repo --release squid
sudo apt update -y
sudo apt install ceph-common -y
ceph -v
sudo vim /etc/ceph/ceph.conf
# PASTE CONFIG

sudo vim /etc/ceph/ceph.keyring
# PASTE AUTH
```

```sh
lsmod | grep rbd
modprobe rbd

rbd -c /etc/ceph/ceph.conf -k /etc/ceph/ceph.keyring -n client.test ls pool --pool test-pool -l 
sudo rbd -n client.test device map --pool test-pool test-volume
# /dev/rbd0

sudo mkfs.ext4 /dev/rbd0
fdisk -l
sudo mount /dev/rbd0 /mnt 
df -h
```

```sh
sudo umount /dev/rdb0
sudo rbd unmap /dev/rbd0
```

