#!/usr/bin/env python

import boto3
import os
import fnmatch
import time
import sys
from os import environ
from botocore.exceptions import ClientError


def get_aws_creds():
    aws_properties = {}

    if "AWS_KEY_ID" in environ and "AWS_SECRET_ACCESS_KEY" and "NINJA_BUCKET_NAME" in environ:
        aws_properties['aws_access_key_id'] = environ['AWS_KEY_ID']
        aws_properties['aws_secret_access_key'] = environ['AWS_SECRET_ACCESS_KEY']
        aws_properties['bucket_name'] = environ['NINJA_BUCKET_NAME']
    else:
        try:
            with open('aws.properties') as property_file:

                for line in property_file:
                    if '=' in line:
                        name, value = line.split('=', 1)
                        aws_properties[name.strip()] = value.strip()
        except IOError as e:
            print(f"I/O error reading aws.properties: {e.errno}, {e.strerror}")

            print("finish script does not have AWS credentials.")

    return aws_properties


def upload_file_to_s3(s3_client, filename, bucket, name, prefix=None):
    print("upload")
    if prefix is not None:
        full_path = str(prefix) + "/" + name
    else:
        full_path = name

    try:
        response = s3_client.upload_file(filename, bucket, full_path)
    except ClientError as e:
        print("An error occurred uploading " + filename)
        print(e)

    print(response)


def publish(sns_client, message_text):
    response = {}

    try:
        response = sns_client.publish(TopicArn='arn:aws:sns:us-east-1:547615480402:RenderComplete', Message=message_text, Subject='Morse Code Shinobi')
    except ClientError as e:
        print("An error occurred publishing an SNS message.")
        print(e)

    print(response)

creds = get_aws_creds()

# upload files to S3
prefix = int(time.time())
s3_client = boto3.client('s3', aws_access_key_id=creds['aws_access_key_id'], aws_secret_access_key=creds['aws_secret_access_key'])
input_directory = os.listdir(sys.argv[1])
mp3_file_pattern = "*.mp3"
for mp3_file in input_directory:
    if fnmatch.fnmatch(mp3_file, mp3_file_pattern):
        upload_file_to_s3(s3_client, sys.argv[1] + '/' + mp3_file, creds['bucket_name'], mp3_file, prefix)

# publish message to SNS
sns_client = boto3.client('sns', region_name='us-east-1', aws_access_key_id=creds['aws_access_key_id'], aws_secret_access_key=creds['aws_secret_access_key'])
message_content = 'Your Morse Code Shinobi render is complete. https://ninja.ki7l.be/view?key=' + str(prefix)
publish(sns_client, message_content)
