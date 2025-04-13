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
