## Memcached for Ubuntu

### controller
```shell
sudo apt install memcached python3-memcache -y 

sudo vim /etc/memcached.conf
-l 172.16.50.41
```
### Finalize installation
```shell
sudo service memcached restart
```