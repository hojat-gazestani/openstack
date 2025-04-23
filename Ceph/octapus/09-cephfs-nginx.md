# Cephfs Nginx
![scenario](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/octapus/PICs/09-ceph-nginx.png)
📡 Cluster Monitoring Commands

Here are monitoring commands to observe the health and state of ceph cluster and cephfs. These tools help you to keep an eye on the cluster status and changes.

```sh
ceph -w
watch ceph orch ps
watch ceph osd pool ls
watch ceph orch ls
```

📦 Create and Authorize CephFS Volume
Create a new CephFS volume `cephfs-nginx` and take a look at its status.

```sh
ceph fs volume create cephfs-nginx

ceph fs ls
ceph mds stat
ceph fs status
```

🔐 CephX client authorization 
The `ceph fs authorize command is used to grant spedific clients controlled access to the CephFS. Here we grants read-wrote access to the root (`/`) of the `cephfs-nginx file system for the client named `client.nginx`.

```sh
ceph fs authorize cephfs-nginx client.nginx / rw
ceph auth get client.nginx

ceph config generate-minimal-conf
```

🔐 CephX Client Configuration

Install required packages on client side and add the required key, and mount the file system using `ceph-fuse. This enable clients to interact with the CephFS volume through a local mount point like `/usr/share/nginx/html/`. 


# CephX
Copy keyring
Copy ceph cluster config

# Client

apt install ceph-fuse ceph-common ceph-fuse


vim /etc/ceph/ceph.keyring
# Paste key here
cleint1 # vim /etc/ceph/ceph.conf
# Paste cluster config here

✅ Mount CephFS on both nodes at `/mnt/cephfs`.
```sh
sudo ceph-fuse --id nginx --keyring /etc/ceph/ceph.keyring --config /etc/ceph/ceph.conf /mnt/cephfs/nginx
sudo ceph-fuse --id nginx /mnt/cephfs
df -h
```

🧪 Shared File System Consistency Test

Verify if multiple NGINX instances (across different nodes/containers) correctly reflect changes made to configuration or content when using a shared CephFS mount.

📌 This Test Is Useful When...
You use CephFS for distributed NGINX content or config delivery

You're deploying load-balanced NGINX servers in a clustered setup

You're validating CephFS as a shared config/content backend


🔍 What's Being Validated

Area    You're Checking
🔄 Real-time sync    Changes in /mnt/cephfs reflect immediately
📁 Shared mount validity Both NGINX servers see and use the same files
🔒 Permission consistency    Files are readable by NGINX on both ends
🧩 Stat cache invalidation   NGINX reloads config/content without restart
🚀 Hot reload test   Whether nginx -s reload picks up new config


Testing step by step


📦 Ensure both NGINX instances include that config file:
```sh
sudo vim /etc/nginx/nginx.conf
include /mnt/cephfs/nginx/*.conf;
```



📝 Edit config on Node A `/mnt/cephfs/nginx/ceph.conf`.

```sh
sudo vim /mnt/cephfs/nginx/ceph.conf

http {
    server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /mnt/cephfs/nginx/var/www/html;

        index ceph.html index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
            try_files $uri $uri/ =404;
        }
    }
}
```

📝 Edit Content on Node A `/mnt/cephfs/nginx/ceph.conf`.

```sh
vim /mnt/cephfs/var/www/html/ceph.html
"Hello from Ceph!"
```


🔁 On Node B, run:

```sh
sudo nginx -t && sudo nginx -s reload
```




















