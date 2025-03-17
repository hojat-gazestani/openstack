# Restart OSD 5 on node 3

```sh
ceph orch ps

osd.5                    ceph-mon3                    running (20h)     7m ago  23h    44.8M    42.4G  19.2.1   f2efb0401a30  4ceae20228dd

```


- On host ceph-mon3

```sh
root@ceph-mon3:/home/hojat# podman ps
CONTAINER ID  IMAGE                                                                                      COMMAND               CREATED       STATUS           PORTS       NAMES
2c5e93ac137b  quay.io/ceph/ceph:v19                                                                                            33 hours ago  Up 33 hours ago              vigorous_meninsky
e0588d038af9  quay.io/ceph/ceph@sha256:41d3f5e46ff7de28544cc8869fdea13fca824dcef83936cb3288ed9de935e4de  -n client.ceph-ex...  33 hours ago  Up 33 hours ago              ceph-e21cad82-01d8-11f0-af3f-092e82507730-ceph-exporter-ceph-mon3
0095385cb363  quay.io/ceph/ceph@sha256:41d3f5e46ff7de28544cc8869fdea13fca824dcef83936cb3288ed9de935e4de  -n client.crash.c...  33 hours ago  Up 33 hours ago              ceph-e21cad82-01d8-11f0-af3f-092e82507730-crash-ceph-mon3
b447bb91fe4b  quay.io/ceph/ceph@sha256:41d3f5e46ff7de28544cc8869fdea13fca824dcef83936cb3288ed9de935e4de  -n mon.ceph-mon3 ...  33 hours ago  Up 33 hours ago              ceph-e21cad82-01d8-11f0-af3f-092e82507730-mon-ceph-mon3
c1d4b9c0bc34  quay.io/ceph/ceph@sha256:41d3f5e46ff7de28544cc8869fdea13fca824dcef83936cb3288ed9de935e4de  -n osd.2 -f --set...  24 hours ago  Up 24 hours ago              ceph-e21cad82-01d8-11f0-af3f-092e82507730-osd-2
4ceae20228dd  quay.io/ceph/ceph@sha256:41d3f5e46ff7de28544cc8869fdea13fca824dcef83936cb3288ed9de935e4de  -n osd.5 -f --set...  20 hours ago  Up 20 hours ago              ceph-e21cad82-01d8-11f0-af3f-092e82507730-osd-5
34ac52fc18e8  quay.io/prometheus/node-exporter:v1.7.0                                                    --no-collector.ti...  11 hours ago  Up 11 hours ago              ceph-e21cad82-01d8-11f0-af3f-092e82507730-node-exporter-ceph-mon3

root@ceph-mon3:/home/hojat# podman restart ceph-e21cad82-01d8-11f0-af3f-092e82507730-osd-5
```
