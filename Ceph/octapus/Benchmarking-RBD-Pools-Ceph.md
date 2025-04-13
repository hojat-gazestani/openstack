# Create a Dummy Image and Benchmark It

## `bench` command

```sh
# Create an image in the SSD pool
rbd create ssd_pool/bench-img --size 1024  # 1GB

# Run the benchmark
rbd bench ssd_pool/bench-img --io-type write --io-size 4K --io-threads 16 --io-total 1G
```

- Repeat the same for the HDD pool:
```sh
rbd create hdd_pool/bench-img --size 1024
rbd bench hdd_pool/bench-img --io-type write --io-size 4K --io-threads 16 --io-total 1G
```

## Use `fio` for More Control

```sh
sudo rbd device map ssd_pool/bench-img

fio --name=write-test --filename=/dev/rbd0 --rw=write --bs=4k --size=1G --numjobs=4 --time_based --runtime=60s --group_reporting
```

## Benchmark RBD with `dd`

```sh
# Write Test (sequential write)
sudo dd if=/dev/zero of=/mnt/testfile bs=1G count=1 oflag=direct

# Read Test (sequential read):

```sh
# First, flush cache and read back the same file:
sudo sync && sudo echo 3 | sudo tee /proc/sys/vm/drop_caches

sudo dd if=/mnt/testfile of=/dev/null bs=1G iflag=direct
```

