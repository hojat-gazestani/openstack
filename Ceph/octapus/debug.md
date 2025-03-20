# Debug

- Cluster
```sh
ceph -s
ceph -w
ceph df
```

- OSD
```sh
ceph osd stat
ceph osd dump
ceph osd tree

ceph orch daemon stop osd.7
ceph orch ps
ceph orch daemon start osd.7
```

```sh
root@ceph-mon3:/home/hojat# ll /var/lib/ceph/e21cad82-01d8-11f0-af3f-092e82507730/
total 816
drwx------ 11 nobody nogroup   4096 Mar 16 09:52 ./
drwxr-xr-x  3 root   root      4096 Mar 16 00:09 ../
-rw-r--r--  1 root   root    787248 Mar 16 00:09 cephadm.c6d8
drwx------  2    167     167   4096 Mar 16 00:33 ceph-exporter.ceph-mon3/
drwxr-xr-x  2 root   root      4096 Mar 16 00:32 config/
drwx------  3 nobody nogroup   4096 Mar 16 00:14 crash/
drwx------  2    167     167   4096 Mar 16 00:33 crash.ceph-mon3/
drw-rw----  2 root   root      4096 Mar 16 00:28 home/
drwx------  3    167     167   4096 Mar 17 10:06 mon.ceph-mon3/
drwx------  3 nobody nogroup   4096 Mar 16 23:10 node-exporter.ceph-mon3/
drwx------  2    167     167   4096 Mar 16 09:52 osd.2/
drwx------  2    167     167   4096 Mar 16 13:26 osd.5/
root@ceph-mon3:/home/hojat# podman ps
CONTAINER ID  IMAGE                        COMMAND               CREATED       STATUS           PORTS       NAMES
2c5e93ac137b  quay.io/ceph/ceph:v19                                                                                            34 hours ago  Up 34 hours ago              vigorous_meninsky
e0588d038af9  quay.io/ceph/ceph@sha256:41  -n client.ceph-ex...  34 hours ago  Up 34 hours ago              ceph-e21cad82-01d8-11f0-af3f-092e82507730-ceph-exporter-ceph-mon3
0095385cb363  quay.io/ceph/ceph@sha256:41  -n client.crash.c...  34 hours ago  Up 34 hours ago              ceph-e21cad82-01d8-11f0-af3f-092e82507730-crash-ceph-mon3
b447bb91fe4b  quay.io/ceph/ceph@sha256:41  -n mon.ceph-mon3 ...  34 hours ago  Up 34 hours ago              ceph-e21cad82-01d8-11f0-af3f-092e82507730-mon-ceph-mon3
c1d4b9c0bc34  quay.io/ceph/ceph@sha256:41  -n osd.2 -f --set...  24 hours ago  Up 24 hours ago              ceph-e21cad82-01d8-11f0-af3f-092e82507730-osd-2
4ceae20228dd  quay.io/ceph/ceph@sha256:41  -n osd.5 -f --set...  21 hours ago  Up 21 hours ago              ceph-e21cad82-01d8-11f0-af3f-092e82507730-osd-5
34ac52fc18e8  quay.io/prometheus/node-exporter:v1.7.0                                                    --no-collector.ti...  11 hours ago  Up 11 hours ago              ceph-e21cad82-01d8-11f0-af3f-092e82507730-node-exporter-ceph-mon3
```


- Mon
```sh
ceph mon stat
ceph mon dump
```

- MDS
```sh
ceph mds stat
```

- PG
```sh
ceph pg stat
ceph pg dump
ceph pg dump pgs
ceph pg dump osds
ceph pg dump pool

ceph pg dump -o /opt/pg --format=json
```

