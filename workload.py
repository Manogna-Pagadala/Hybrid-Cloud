import os

import boto3
from boto3 import client as boto3_client

# cd '/mnt/hgfs/Project 3/test/' && python3 './workload.py'
input_bucket = "cc-project-input-bucket"
output_bucket = "cc-project-output-bucket"
test_cases = "test_cases/"

AWS_ACCESS_KEY_ID_S3 = 'QQ5MU4UW420K61IBE2QT'
AWS_SECRET_ACCESS_KEY_S3 = 'Hmh4BkgN2MXg8RxgibYuKm5teWyaTaiDhAKMA8Uv'

#RGW_URL = os.getenv('RGW_URL')
#AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')


s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID_S3,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY_S3,
    endpoint_url='http://10.0.2.15:8081',  # Specify your S3-compatible endpoint
)

print(s3)
def clear_input_bucket():
    global input_bucket
    list_obj = s3.list_objects_v2(Bucket=input_bucket)
    try:
        for item in list_obj["Contents"]:
            key = item["Key"]
            s3.delete_object(Bucket=input_bucket, Key=key)
    except:
        print("Nothing to clear in input bucket")


def clear_output_bucket():
    global output_bucket
    list_obj = s3.list_objects_v2(Bucket=output_bucket)
    try:
        for item in list_obj["Contents"]:
            key = item["Key"]
            s3.delete_object(Bucket=output_bucket, Key=key)
    except:
        print("Nothing to clear in output bucket")

    clear_local_output()


def clear_local_output():
    os.system("rm -rf /tmp/csv")


def upload_to_input_bucket_s3(path, name):
    global input_bucket
    s3.upload_file(path + name, input_bucket, name)


def upload_files(test_case):
    global input_bucket
    global output_bucket
    global test_cases

    # Directory of test case
    test_dir = test_cases + test_case + "/"

    # Iterate over each video
    # Upload to S3 input bucket
    for filename in os.listdir(test_dir):
        if filename.endswith(".mp4") or filename.endswith(".MP4"):
            print("Uploading to input bucket..  name: " + str(filename))
            upload_to_input_bucket_s3(test_dir, filename)


def workload_generator():

    # print("Running Test Case 1")
    # upload_files("test_case_1")

    print("Running Test Case 2")
    upload_files("test_case_2")


# clear_input_bucket()
# clear_output_bucket()
workload_generator()