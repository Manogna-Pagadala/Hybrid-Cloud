import requests

import boto3



access_key = 'QQ5MU4UW420K61IBE2QT'

secret_key = 'Hmh4BkgN2MXg8RxgibYuKm5teWyaTaiDhAKMA8Uv'



# Create an S3 client

s3 = boto3.client(

    's3',

    aws_access_key_id=access_key,

    aws_secret_access_key=secret_key,

    endpoint_url='http://10.0.2.15:8081',  # Specify your S3-compatible endpoint

)



# Specify the bucket name

bucket_name = 'cc-project-input-bucket'



# List all objects in the bucket

response = s3.list_objects_v2(Bucket=bucket_name)


# URL of the OpenFaaS function

url = "http://localhost:8082/function/face-recognition"

# Print the object names

print("Object names in the bucket:")

for obj in response.get('Contents', []):

    print(obj['Key'])
    payload = {"bucket": "cc-project-input-bucket", "object": obj["Key"]}
    headers = {"Content-Type": "application/json"}
    try:

        response = requests.post(url, json=payload, headers=headers)

        # Handle the response as needed

        print(f"Object: {obj}, Status Code: {response.status_code}, Response: {response.text}")

    except requests.RequestException as e:

        print(f"Object: {obj}, Error: {e}")