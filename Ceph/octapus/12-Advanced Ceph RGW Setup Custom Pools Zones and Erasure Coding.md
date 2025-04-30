# Advanced Ceph RGW Setup with Custom Pools and Erasure Coding

Advanced approach to configuring Ceph's RADOS Gateway (RGW). It begins with customization of zone configurations. A key aspect covered is the creation of erasure coding profiles for data protection. The guide also touches upon user creation within the gateway and utilizing the AWS S3 CLI for interacting with the Ceph object storage. Finally, briefly simulating failures, suggesting a focus on resilience and testing.

![basic](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/octapus/PICs/16-ceph-aws-cli-rgw.png)


## Deploy New RGW Service
the process for setting up and deploying a new instance of the Ceph RADOS Gateway service
- Deploy a basic RADOS Gateway (RGW) instance using Ceph Orchestrator.
setting up Ceph RADOS Gateway (RGW) with custom storage pools and erasure coding for data protection

```sh
# Modify zone settings to point to new pools.
ceph orch apply rgw rgw-advanced

# Create a fresh RGW instance for a clean setup.
ceph osd pool ls | grep rgw
```

## Customize Zone Configuration

- how to modify and tailor the zone settings within the Ceph RGW environment to meet specific requirements

```sh
radosgw-admin zone get > rgw-advanced.json

vim rgw-advanced.json

:%s/default\./advanced./g

:%s/"name": "default"/"name": "culster"/g

radosgw-admin zone set < rgw-advanced.json
radosgw-admin zone get

ceph osd pool ls

# Restart the RGW service to apply zone changes.
ceph orch restart rgw.rgw-advanced

for pool in $(ceph osd pool ls | grep default); do echo osd pool rm "${pool}" "${pool}" --yes-i-really-really-mean-it ; done

ceph osd pool ls
```

```sh
ceph osd erasure-code-profile ls
ceph osd erasure-code-profile get default
```

## Create Erasure Coding Profile

outlines the procedure for defining and establishing an erasure coding profile, which is a method for data redundancy and storage efficiency

```sh
# Define an erasure coding profile for better storage efficiency.
ceph osd erasure-code-profile set rgw-ecp-advanced k=2 m=1 crush-failure-domain=host

ceph osd erasure-code-profile get rgw-ecp-advanced

# Create and enable a new erasure-coded pool for RGW data.
ceph osd pool create advanced.rgw.buckets.data erasure rgw-ecp-advanced

ceph osd pool ls detail | grep erasure

ceph osd pool application enable advanced.rgw.buckets.data rgw

ceph osd pool ls
``` 


# ceph rados gateway create user

command-line instruction used to add and manage new users within the Ceph RADOS Gateway system

```sh
radosgw-admin user create --uid={username} --display-name="{display-name}" 

radosgw-admin user create --uid=s3user-advanced --display-name="s3user Adv" 

radosgw-admin user list
radosgw-admin user info --uid s3user-advanced


```

# AWS S3 CLI for Ceph Object Gateway Storage

describes how to utilize the AWS S3 command-line interface tools to interact with and manage storage within the Ceph Object Gateway

```sh
aws configure --profile=s3user-advanced
access_key: # PAST ACCESS_KEY
secret_key: # PAST SECRET_KEY
output format: json

cat ~/.aws/config
cat ~/.aws/credentials
```

```sh
aws --profile rgwuser-basic --endpoint-url  http://192.168.1.1 s3 ls

# Create buckets and upload files to Ceph RGW via AWS CLI.
aws --profile rgwuser-basic --endpoint-url  http://192.168.1.1 s3 mb s3://bucketadvance

# Run on ceph cluster to Confirm that the bucket and objects exist in Ceph directly.
radosgw-admin bucket list 

aws --profile s3user-advanced --endpoint-url  http://192.168.1.1 s3api put-object --bucket bucketadvance

aws --profile s3user-advanced --endpoint-url  http://192.168.1.1 s3api list-object --bucket bucketadvance --key testfile --body /var/www/objects    

# Run on ceph cluster to verify
radosgw-admin bucket stats | grep num_objects
```

```sh
ceph osd pool ls
```

```sh
dd if=/dev/zero of=100mb.file bs=1M count=100

BUCKET_NAME=buckebasic
RGW_ENDPOINT=http://192.168.1.1
time aws s3 cp 100mb.file s3://${BUCKET_NAME}/ --endpoint-url=${RGW_ENDPOINT}

BUCKET_NAME=bucketadvance
time aws s3 cp 100mb.file s3://${BUCKET_NAME}/ --endpoint-url=${RGW_ENDPOINT}
```


## Simulate Failures

 testing the resilience and stability of the Ceph RGW setup by simulating various types of failures

```sh
ceph osd set noout          # Prevent data rebalancing
ceph osd down osd.0         # Kill an OSD
aws s3 ls s3://${BUCKET_NAME}/ --endpoint-url=${RGW_ENDPOINT}  # Access still works
ceph osd unset noout

```



## python boto3
demonstrates how to interact with the Ceph Object Gateway Storage (RGW) using the boto3 library after the S3 client has been initialized
 practical ways to manage objects within your Ceph RGW storage programmatically using Python and the boto3 library
 utilizing the "AWS S3 CLI for Ceph Object Gateway Storage" for managing your object storage. While this example uses Python, the underlying concepts of uploading, listing, and generating pre-signed URLs are analogous to operations performed using the AWS S3 command-line interface.

```py
import boto3
import os

# Load config from env
config = {
    'endpoint_url': os.environ['RGW_ENDPOINT'],
    'aws_access_key_id': os.environ['AWS_ACCESS_KEY_ID'],
    'aws_secret_access_key': os.environ['AWS_SECRET_ACCESS_KEY']
}

# Initialize S3 client
s3 = boto3.client('s3', **config)

# Test connection
try:
    s3.list_buckets()
    print("✅ Successfully connected to RGW!")
except Exception as e:
    print(f"❌ Connection failed: {str(e)}")

s3 = boto3.client(
    's3',
    endpoint_url='http://your-rgw:8080',
    aws_access_key_id='ACCESS_KEY',
    aws_secret_access_key='SECRET_KEY'
)

# Upload
s3.upload_file('100mb.file', 'bucket', '100mb.file')

# List objects
response = s3.list_objects(Bucket='bucket')
for obj in response['Contents']:
    print(obj['Key'])

# Generate pre-signed URL (time-limited access)
url = s3.generate_presigned_url('get_object', Params={'Bucket': 'bucket', 'Key': '100mb.file'}, ExpiresIn=3600)
print(url)
```





## Remove Default RGW Pools


the steps involved in deleting the standard storage pools that are automatically created when a basic RADOS Gateway instance is deployed using the Ceph Orchestrator

```sh
ceph config set mon mon_allow_pool_delete true
for pool in $(ceph osd pool ls | grep rgw); do echo "${pool}" ; done

for pool in $(ceph osd pool ls | grep rgw); do echo osd pool rm "${pool}" "${pool}" --yes-i-really-really-mean-it ; done

ceph osd pool ls
``` 

