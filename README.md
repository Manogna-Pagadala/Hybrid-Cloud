# Smart Classroom Assistant – Hybrid Cloud Face Recognition System

A hybrid-cloud, serverless face recognition application built using **OpenFaaS, Kubernetes, Minikube, Helm, Ceph Object Storage, AWS DynamoDB, Docker, and Python**.

The system processes classroom videos uploaded to Ceph object storage, identifies student faces, retrieves corresponding student information from DynamoDB, and generates CSV reports automatically.

By combining self-hosted serverless computing with cloud database services, the application demonstrates event-driven processing across a hybrid-cloud architecture.

## Overview

The Smart Classroom Assistant is designed to automate student identification and academic information retrieval from classroom videos.

When a video is uploaded to the Ceph RGW input bucket, the application:

1. Detects the new video through a bucket-monitoring application.
2. Invokes a face recognition function deployed on OpenFaaS.
3. Downloads the video and extracts frames using FFmpeg.
4. Identifies students by comparing detected faces against known face encodings.
5. Retrieves matching student information from Amazon DynamoDB.
6. Generates a CSV file containing the identified student's details.
7. Uploads the CSV result to the Ceph RGW output bucket.

The system uses **OpenFaaS on Kubernetes** for serverless function execution, **Ceph RGW** for object storage, and **Amazon DynamoDB** for student information retrieval.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Face recognition and application logic |
| OpenFaaS | Serverless function deployment and execution |
| Kubernetes | Container orchestration |
| Minikube | Local Kubernetes environment |
| Helm | OpenFaaS installation and configuration |
| Ceph / MicroCeph | Distributed object storage infrastructure |
| Ceph RADOS Gateway (RGW) | S3-compatible video and CSV storage |
| Amazon DynamoDB | Student information database |
| Docker | Containerizing the face recognition function |
| Docker Hub | Hosting the function's container image |
| FFmpeg | Extracting video frames |
| face_recognition | Identifying faces using known encodings |
| boto3 | Interacting with object storage and AWS services |
| faas-cli | Deploying and managing OpenFaaS functions |

## System Architecture

```text
                  Classroom Video Upload
                            |
                            v
                   Ceph RGW Input Bucket
                            |
                            v
                 Bucket Monitoring Application
                         (trigger.py)
                            |
                            v
                      OpenFaaS Gateway
                            |
                            v
                Face Recognition Function
                 (Kubernetes / Minikube)
                            |
                            v
                  Download Input Video
                            |
                            v
                  Extract Frames (FFmpeg)
                            |
                            v
                 Face Recognition Processing
                            |
                            v
                     AWS DynamoDB
                 Retrieve Student Details
                            |
                            v
                    Generate CSV Report
                            |
                            v
                  Ceph RGW Output Bucket
```

The OpenFaaS function runs as a containerized workload in Kubernetes, while Ceph provides object storage and DynamoDB provides student records.

## Key Features

### 1. Hybrid-Cloud Architecture

The application combines locally deployed cloud infrastructure with managed AWS services.

- **OpenFaaS:** Executes serverless functions on Kubernetes.
- **Ceph RGW:** Stores input videos and generated CSV reports.
- **Amazon DynamoDB:** Stores student information for lookup.

This architecture demonstrates how self-hosted infrastructure and managed cloud services can work together within one application.

### 2. Event-Driven Video Processing

A bucket-monitoring application detects new videos uploaded to the Ceph RGW input bucket and triggers the OpenFaaS function.

Each detected upload initiates the video processing workflow without requiring manual function execution.

### 3. Serverless Computing with OpenFaaS

The face recognition function is deployed using OpenFaaS on a Minikube Kubernetes cluster.

The OpenFaaS environment is configured using Helm, Kubernetes namespaces, authentication credentials, and secrets.

Functions are packaged as Docker images and deployed using the OpenFaaS CLI.

### 4. Video Frame Extraction and Face Recognition

The application uses FFmpeg to extract frames from uploaded videos.

The Python `face_recognition` library compares detected faces against stored face encodings to identify students.

The identified names are then used to retrieve corresponding student information from DynamoDB.

### 5. Student Information Retrieval

Student records are stored in an Amazon DynamoDB table named `student1`.

The database contains fields such as:

- Name
- Student ID
- Major
- Year

After identifying a student, the application retrieves the corresponding record and generates a CSV report containing the student's name, major, and year.

### 6. Ceph Object Storage Integration

The system uses Ceph RADOS Gateway (RGW) for S3-compatible object storage.

Two buckets are configured:

- **Input bucket:** Stores classroom videos awaiting processing.
- **Output bucket:** Stores generated CSV reports.

Output files follow a naming convention associated with their original input videos.

## Project Structure

The main components described in the project are:

```text
.
├── handler.py
├── trigger.py
├── workload.py
├── upload_data.py
├── face-recognition.yml
├── requirements.txt
├── student_data.json
└── README.md
```

The layout above illustrates the main project files. The actual repository may also include Docker configuration, face encodings, and additional deployment files.

### handler.py

Contains the face recognition function deployed through OpenFaaS.

Its responsibilities include:

1. Receiving information about the uploaded video.
2. Retrieving the video from the Ceph RGW input bucket.
3. Extracting frames using FFmpeg.
4. Performing face recognition against known face encodings.
5. Querying DynamoDB for matching student records.
6. Generating a CSV report.
7. Uploading the CSV to the Ceph RGW output bucket.

### trigger.py

Monitors the Ceph RGW input bucket and invokes the OpenFaaS face recognition function when new videos are detected.

This component connects object storage events with serverless function execution.

### workload.py

Uploads videos to the Ceph RGW input bucket for application testing.

It is used to evaluate the end-to-end processing workflow with different numbers of uploaded videos.

### upload_data.py

Loads student information from `student_data.json` into DynamoDB.

The script uses boto3 to insert student records into the `student1` table.

### face-recognition.yml

Defines the OpenFaaS function configuration, including the function's image and deployment settings.

### requirements.txt

Lists Python dependencies required by the face recognition function.

## Installation and Deployment

### Prerequisites

- Python
- Docker
- Kubernetes
- Minikube
- Helm
- OpenFaaS CLI (`faas-cli`)
- MicroCeph with RGW enabled
- AWS account with DynamoDB access
- AWS credentials and Ceph RGW access credentials
- Known face encodings
- Classroom video files for testing

### Step 1: Start Minikube

Start a local Kubernetes cluster:

```bash
minikube start
```

Verify that the cluster is running:

```bash
kubectl get nodes
```

### Step 2: Install OpenFaaS

Add the OpenFaaS Helm repository:

```bash
helm repo add openfaas https://openfaas.github.io/faas-netes/
helm repo update
```

Create the required Kubernetes namespaces:

```bash
kubectl create namespace openfaas
kubectl create namespace openfaas-fn
```

Configure the OpenFaaS authentication secret and deploy OpenFaaS using Helm.

The exact Helm values depend on the OpenFaaS version and cluster configuration.

### Step 3: Configure OpenFaaS Access

Configure access to the OpenFaaS gateway and authenticate using `faas-cli`.

For a local deployment, the gateway can be accessed through Kubernetes port forwarding:

```bash
kubectl port-forward -n openfaas svc/gateway 8080:8080
```

Then authenticate using the credentials configured during installation.

### Step 4: Configure Ceph Object Storage

Install MicroCeph and configure the Ceph RADOS Gateway service.

Create the required input and output buckets.

Configure the RGW endpoint and access credentials so the application can upload and retrieve objects.

### Step 5: Configure DynamoDB

Create a DynamoDB table named `student1` and populate it with student records.

```bash
python upload_data.py
```

The script reads records from `student_data.json` and inserts them into DynamoDB.

### Step 6: Build and Deploy the OpenFaaS Function

The face recognition function uses the OpenFaaS `python3-debian` template and includes the dependencies required for video processing and facial recognition.

Build and push the function image:

```bash
faas-cli build -f face-recognition.yml
faas-cli push -f face-recognition.yml
```

Deploy the function:

```bash
faas-cli deploy -f face-recognition.yml
```

The Docker image must be configured with an accessible container registry and appropriate credentials.

### Step 7: Configure the Trigger

Configure the bucket-monitoring application with:

- Ceph RGW endpoint
- Input bucket name
- Ceph access credentials
- OpenFaaS gateway address
- Face recognition function name

Run the trigger application to monitor incoming videos.

```bash
python trigger.py
```

### Step 8: Run the Workload Generator

Configure the workload generator with the Ceph RGW endpoint, input bucket, and credentials.

```bash
python workload.py
```

The workload generator uploads videos to the input bucket, initiating the processing workflow.

### Step 9: Verify Results

After processing completes, inspect the Ceph RGW output bucket.

Each processed video should produce a corresponding CSV report containing the identified student information.

## Testing and Evaluation

The application was tested with two workloads to verify video processing, face recognition, DynamoDB integration, and output generation.

| Test case | Videos uploaded | Expected workflow |
|---|---:|---|
| Test 1 | 8 | OpenFaaS invocation, face recognition, DynamoDB lookup, CSV generation |
| Test 2 | 100 | Processing of a larger workload through the same pipeline |

### Validation

Testing covered:

- Uploading videos to the Ceph RGW input bucket.
- Detecting new videos through the monitoring application.
- Invoking the OpenFaaS function.
- Extracting video frames and identifying faces.
- Retrieving student information from DynamoDB.
- Generating CSV reports.
- Verifying output files in the Ceph RGW output bucket.

The number of OpenFaaS function invocations was observed to correspond to the number of videos uploaded during testing.

## Project Outcome

The Smart Classroom Assistant demonstrates an event-driven, hybrid-cloud application that combines serverless computing, object storage, and managed database services.

The project covers:

- Deploying OpenFaaS on Kubernetes using Helm.
- Managing serverless functions in a containerized environment.
- Integrating Ceph RGW object storage with event-triggered processing.
- Performing video frame extraction and face recognition.
- Retrieving student information from Amazon DynamoDB.
- Generating CSV reports automatically.
- Testing the application with workloads of 8 and 100 videos.

The implementation provides practical experience with hybrid-cloud architecture, Kubernetes orchestration, serverless function deployment, and distributed application integration.

## Technologies Used

`Python` · `OpenFaaS` · `Kubernetes` · `Minikube` · `Helm` · `Ceph` · `MicroCeph` · `Ceph RGW` · `AWS DynamoDB` · `Docker` · `Docker Hub` · `boto3` · `FFmpeg` · `face_recognition`
