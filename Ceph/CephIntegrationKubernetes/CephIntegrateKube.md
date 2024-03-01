# Ceph Integrate Kubernetes

## CREATE A POOL
```sh
ceph osd pool create kubernetes
rbd pool init kubernetes
```

## CONFIGURE CEPH-CSI

### SETUP CEPH CLIENT AUTHENTICATION
```sh
ceph auth get-or-create client.kubernetes mon 'profile rbd' osd 'profile rbd pool=kubernetes' mgr 'profile rbd pool=kubernetes'
```
### GENERATE CEPH-CSI CONFIGMAP
+ ceph-csi currently only supports the legacy V1 protocol.

+ kubernetes cluster information
```sh
kubectl version --short

Client Version: v1.27.3
Kustomize Version: v5.0.1
Server Version: v1.27.3
```

```sh
kubectl get ns kube-system -o jsonpath='{.metadata.uid}'
ff90b61b-9e53-45ca-a7a1-966a6b5e0696
```

```sh
ceph mon dump
```

```sh
cat <<EOF > csi-config-map.yaml
---
apiVersion: v1
kind: ConfigMap
data:
  config.json: |-
    [
      {
        "clusterID": "ff90b61b-9e53-45ca-a7a1-966a6b5e0696",
        "monitors": [
          "192.168.56.81:6789",
          "192.168.56.82:6789",
          "192.168.56.83:6789"
        ]
      }
    ]
metadata:
  name: ceph-csi-config
EOF

kubectl apply -f csi-config-map.yaml
```

```sh
$ cat <<EOF > csi-kms-config-map.yaml
---
apiVersion: v1
kind: ConfigMap
data:
  config.json: |-
    {}
metadata:
  name: ceph-csi-encryption-kms-config
EOF

kubectl apply -f csi-kms-config-map.yaml
```

```sh
cat <<EOF > ceph-config-map.yaml
---
apiVersion: v1
kind: ConfigMap
data:
  ceph.conf: |
    [global]
    auth_cluster_required = cephx
    auth_service_required = cephx
    auth_client_required = cephx
  # keyring is a required key and its value should be empty
  keyring: |
metadata:
  name: ceph-config
EOF

kubectl apply -f ceph-config-map.yaml
```

### GENERATE CEPH-CSI CEPHX SECRET

```sh
cat <<EOF > csi-rbd-secret.yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: csi-rbd-secret
  namespace: default
stringData:
  userID: kubernetes
  userKey: AQD9o0Fd6hQRChAAt7fMaSZXduT3NWEqylNpmg==
EOF

kubectl apply -f csi-rbd-secret.yaml
```

### CONFIGURE CEPH-CSI PLUGINS

```sh
kubectl apply -f https://raw.githubusercontent.com/ceph/ceph-csi/master/deploy/rbd/kubernetes/csi-provisioner-rbac.yaml
kubectl apply -f https://raw.githubusercontent.com/ceph/ceph-csi/master/deploy/rbd/kubernetes/csi-nodeplugin-rbac.yaml
```

```sh
wget https://raw.githubusercontent.com/ceph/ceph-csi/master/deploy/rbd/kubernetes/csi-rbdplugin-provisioner.yaml
kubectl apply -f csi-rbdplugin-provisioner.yaml

wget https://raw.githubusercontent.com/ceph/ceph-csi/master/deploy/rbd/kubernetes/csi-rbdplugin.yaml
kubectl apply -f csi-rbdplugin.yaml
```

## USING CEPH BLOCK DEVICES

### CREATE A STORAGECLASS
```sh
cat <<EOF > csi-rbd-sc.yaml
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
   name: csi-rbd-sc
provisioner: rbd.csi.ceph.com
parameters:
   clusterID: b9127830-b0cc-4e34-aa47-9d1a2e9949a8
   pool: kubernetes
   imageFeatures: layering
   csi.storage.k8s.io/provisioner-secret-name: csi-rbd-secret
   csi.storage.k8s.io/provisioner-secret-namespace: default
   csi.storage.k8s.io/controller-expand-secret-name: csi-rbd-secret
   csi.storage.k8s.io/controller-expand-secret-namespace: default
   csi.storage.k8s.io/node-stage-secret-name: csi-rbd-secret
   csi.storage.k8s.io/node-stage-secret-namespace: default
reclaimPolicy: Delete
allowVolumeExpansion: true
mountOptions:
   - discard
EOF

kubectl apply -f csi-rbd-sc.yaml
```

### CREATE A PERSISTENTVOLUMECLAIM

```sh
cat <<EOF > raw-block-pvc.yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: raw-block-pvc
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Block
  resources:
    requests:
      storage: 1Gi
  storageClassName: csi-rbd-sc
EOF
kubectl apply -f raw-block-pvc.yaml
```

```sh
cat <<EOF > raw-block-pod.yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-raw-block-volume
spec:
  containers:
    - name: fc-container
      image: fedora:26
      command: ["/bin/sh", "-c"]
      args: ["tail -f /dev/null"]
      volumeDevices:
        - name: data
          devicePath: /dev/xvda
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: raw-block-pvc
EOF
kubectl apply -f raw-block-pod.yaml
```

```sh
cat <<EOF > pvc.yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: rbd-pvc
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 1Gi
  storageClassName: csi-rbd-sc
EOF
kubectl apply -f pvc.yaml


```sh
cat <<EOF > pod.yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: csi-rbd-demo-pod
spec:
  containers:
    - name: web-server
      image: nginx
      volumeMounts:
        - name: mypvc
          mountPath: /var/lib/www/html
  volumes:
    - name: mypvc
      persistentVolumeClaim:
        claimName: rbd-pvc
        readOnly: false
EOF
kubectl apply -f pod.yaml
```

[1]: https://docs.ceph.com/en/latest/rbd/rbd-kubernetes/
