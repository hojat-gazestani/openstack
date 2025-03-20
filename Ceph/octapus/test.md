# Test

```sh
dd if=/dev/random of=./bigfile bs=100M count=10     # 1 Gig
dd if=/dev/random of=./bigfile bs=10M count=100     # 1 Gig
dd if=/dev/random of=./bigfile bs=1M count=200      # 200 M

for number in {1..100}; do echo "${number}"; done
for number in {1..100}; do dd if=/dev/random of=/opt/file_"{$number}" bs=10M count=3; done

while true; do echo $(head -c 1000 / dev/urandom | tr -dc 'a-zA-Zo-9~!@#$%^&*_-' | fold -w 15 | head n 1) >> /opt/testfile; cat /opt/testfi
le › /dev/null; echo $(date) ; sleep 1; done



```