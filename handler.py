from boto3 import client as boto3_client
import boto3
import face_recognition
import pickle
import os
import csv
import json

input_bucket = "cc-project-input-bucket"
output_bucket = "cc-project-output-bucket"

access_key_s3 = 'QQ5MU4UW420K61IBE2QT'
secret_key_s3 = 'Hmh4BkgN2MXg8RxgibYuKm5teWyaTaiDhAKMA8Uv'

# Create an S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=access_key_s3,
    aws_secret_access_key=secret_key_s3,
    endpoint_url='http://10.0.2.15:8081',  # Specify your S3-compatible endpoint
)


accesskey='AKIAX643R3BDZ34JHUR2'
secretkey='rj0HSIx2rASmjpQm1LH4kSkyuQm28B/mFaWF7jKT'
region='us-east-1'

#s3 = boto3_client('s3', aws_access_key_id=accesskey, aws_secret_access_key=secretkey, region_name=region)
dynamodb = boto3.resource('dynamodb', aws_access_key_id=accesskey, aws_secret_access_key=secretkey, region_name=region)

def query_write_to_s3(face, video):
	table = dynamodb.Table('student1')
	header = ['name', 'major', 'year']
	try:
		result = table.get_item(Key={'name': face})
		#print("Item found: ",result['Item'])
		name = result['Item']['name']
		major = result['Item']['major']
		year = result['Item']['year']
		row = [name, major, year]
		path = "/tmp/" + video + ".csv"
		with open(path, 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(header)
			writer.writerow(row)
		#print('Uploading ' + path + 'to output s3 bucket')
		s3.upload_file(path, 'cc-project-output-bucket', video + ".csv")

	except Exception as e:
		print("Error querying DynamoDB:", str(e))

def handle(event):	
	#print(event)
	event_data = json.loads(event)
	bucket =event_data['bucket']#"cc-project-input-bucket" #event['Records'][0]['s3']['bucket']['name']
	object =event_data['object'] #"test_0.mp4" #event['Records'][0]['s3']['object']['key']
	#print(object)
	tmp_path ='/tmp/'
	video = tmp_path + object
	#print(video)

	with open(video, 'wb') as data:
		s3.download_fileobj(bucket, object, data)

	frames_path = '/tmp/frames/'+object.split(".")[0]+'/'
	if not os.path.exists(frames_path):
		os.makedirs(frames_path)
	# Execute FFmpeg command to extract frames
	os.system("ffmpeg -i " + video + " -r 1 " + frames_path + "image-%3d.jpeg")
	frames = os.listdir(frames_path)
	#print("num frames",len(frames),frames_path,frames)
	for frame in frames:
		#print('Processing frame:',frame )
		img = face_recognition.load_image_file(frames_path+frame)
		frame_encodings = face_recognition.face_encodings(img)
		if len(frame_encodings)>0:
			img_encoding = frame_encodings[0]
			break
	#print('image encoding: ',len(img_encoding),img_encoding)
	
        #local_encoding_file = os.path.join(os.path.dirname(file), 'encoding')
	file = open("function/encoding","rb") #open('/home/app/encoding', "rb") 
	known_encodings = pickle.load(file)
	file.close()

	result = face_recognition.compare_faces(known_encodings['encoding'], img_encoding)
	ind = 0
	for index, value in enumerate(result):
		if value:
			ind=index
			break
	face = list(known_encodings['name'])[ind]
	#print("Recognized face: ",face)
	query_write_to_s3(face, object.split(".")[0])