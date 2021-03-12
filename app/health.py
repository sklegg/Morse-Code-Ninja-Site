#!/usr/bin/env python

import sys
import boto3
import botocore
from os import environ

# define return codes
OK = 0
ERROR = 1

# todo: move to a common library module
def get_aws_creds():
    aws_properties = {}

    aws_properties['aws_session_token'] = None
    if "AWS_SESSION_TOKEN" in environ:
        aws_properties['aws_session_token'] = environ['AWS_SESSION_TOKEN']

    if "AWS_KEY_ID" in environ and "AWS_SECRET_ACCESS_KEY" in environ:
        aws_properties['aws_access_key_id'] = environ['AWS_KEY_ID']
        aws_properties['aws_secret_access_key'] = environ['AWS_SECRET_ACCESS_KEY']
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


# make a client with the existing creds
current_creds = get_aws_creds()
try:
    sts = boto3.client('sts', aws_access_key_id=current_creds['aws_access_key_id'], aws_secret_access_key=current_creds['aws_secret_access_key'], aws_session_token=current_creds['aws_session_token'])
    sts.get_caller_identity()
    print(OK)
    sys.exit(OK)
except KeyError as e:
    print(ERROR)
    sys.exit(OK)
except botocore.exceptions.ClientError as e:
    print(ERROR)
    sys.exit(OK)
