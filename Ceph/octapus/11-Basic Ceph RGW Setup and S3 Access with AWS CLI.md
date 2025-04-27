# Basic Ceph RGW Setup and S3 Access with AWS CLI

The foundational steps for setting up a Ceph RADOS Gateway (RGW). The deployment of the RGW service using the Ceph Orchestrator. Furthermore, covers the creation of a basic RGW user and the process of connecting to the RGW endpoint utilizing the AWS Command Line Interface (CLI). Finally, indicates it will explain how to upload, list, and generally manage objects within this environment.

# Deploy RGW service

The initial setup and deployment of a RADOS Gateway (RGW) instance within a Ceph storage cluster using the Ceph Orchestrator

- Deploy a basic RADOS Gateway (RGW) instance using Ceph Orchestrator.

```sh
# Deploy a basic RADOS Gateway (RGW) instance using Ceph Orchestrator.
ceph orch apply rgw rgw-basic

# Verify that the RGW service is up and running correctly.
ceph -s | grep rgw
ceph orch ls | grep rgw
ceph orch ps | grep rgw

# See the default pools automatically created for RGW.
ceph osd pool ls | grep rgw
# TODO How seperate rgw pools
```


# Create a simple RGW user
The process of creating a basic user account specifically for accessing the RGW service,  with associated credentials and permissions

```sh
# Create a user account for accessing RGW S3-compatible storage.
radosgw-admin user create --uid={username} --display-name="{display-name}" 

radosgw-admin user create --uid=rgwuser-basic --display-name="RGWuser Basic"

radosgw-admin user list
radosgw-admin user info --uid rgwuser-basic


```

# Connect to RGW endpoint using AWS CLI

How to configure and utilize the aws Command Line Interface (AWS CLI) to establish a connection with the deployed RGW endpoint, enabling interaction with the Ceph object storage

```sh
# Set up AWS CLI to interact with the Ceph RGW endpoint.
aws configure --profile=rgwuser-basic
access_key: # PAST ACCESS_KEY
secret_key: # PAST SECRET_KEY
output format: json

cat ~/.aws/config
cat ~/.aws/credentials

aws --profile rgwuser-basic --endpoint-url  http://192.168.1.1 s3 ls

# Create buckets and upload files to Ceph RGW via AWS CLI.
aws --profile rgwuser-basic --endpoint-url  http://192.168.1.1 s3 mb s3://buckebasic

# Run on ceph cluster to Confirm that the bucket and objects exist in Ceph directly.
radosgw-admin bucket list 
```

# Upload, list, and manage objects

the subsequent steps after establishing a connection, including performing common object storage operations such as uploading data, listing the stored objects, and other management tasks using the AWS CLI against the Ceph RGW

```sh

BUCKET_NAME=buckebasic
RGW_ENDPOINT=http://192.168.1.1

aws --profile rgwuser-basic --endpoint-url  ${BUCKET_NAME} s3api put-object --bucket ${RGW_ENDPOINT}

aws --profile rgwuser-basic --endpoint-url  ${BUCKET_NAME} s3api list-object --bucket ${RGW_ENDPOINT} --key testfile --body /etc/services

time aws s3 cp largefile s3://${BUCKET_NAME}/ --endpoint-url=${RGW_ENDPOINT}

# Run on ceph cluster to verify
ceph osd pool get cluster.rgw.buckets.data all

radosgw-admin bucket stats | grep num_objects
```

```sh
dd if=/dev/zero of=100mb.file bs=1M count=100

BUCKET_NAME=buckebasic
RGW_ENDPOINT=http://192.168.1.1
time aws s3 cp 100mb.file s3://${BUCKET_NAME}/ --endpoint-url=${RGW_ENDPOINT}

```

```sh
radosgw-admin bucket list 
radosgw-admin bucket stats

```


```sh
for num in {1..50}: do aws --profile rgwuser-basic --endpoint-url  http://192.168.1.1 s3api list-object --bucket buckebasic --key testfile"${num}" --body /etc/services; done

radosgw-admin bucket stats | grep num_objects

ceph -s | grep objects
```

```sh
for num in {1..50}: do aws --profile rgwuser-basic --endpoint-url  http://192.168.1.1 s3api delete-object --bucket buckebasic --key testfile"${num}" ; done

``` 


```sh
ceph osd pool ls | grep replicated

eph osd pool ls detail 
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




