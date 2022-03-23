## Backup - cinder

```shell
sudo apt install cinder-backup

sudo vim /etc/cinder/cinder.conf
[DEFAULT]
# ...
backup_driver = cinder.backup.drivers.swift
backup_swift_url = SWIFT_URL



````

```shell
openstack catalog show object-store
````

### Finalize installation

```shell
sudo service cinder-backup restart
````