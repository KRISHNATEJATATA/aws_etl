#creating s3 buckets
import boto3
import json
import os
s3_client = boto3.client('s3')
response = s3_client.create_bucket(
    ACL='private',
    Bucket='s3_etl_source')
response = s3_client.create_bucket(
    ACL='private',
    Bucket='s3-etl-target')
# create iam role use aws service as glue give s3 full access ,glue service role
iam_client = boto3.client('iam')
policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "glue.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
}
response = iam_client.create_role(RoleName='aws_etl_s3', AssumeRolePolicyDocument= json.dumps(policy),)
s3_full_access='arn:aws:iam::aws:policy/AmazonS3FullAccess'
glue_service_role='arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole'
response = iam_client.attach_role_policy(
    RoleName='aws_etl_s3',
    PolicyArn=s3_full_access
)
response = iam_client.attach_role_policy(
    RoleName='aws_etl_s3',
    PolicyArn=glue_service_role
)
# Define the relative path to the folder
file=os.getcwd()
file=file.replace('\\','/')
file+='/enterprise'
response=s3_client.upload_file(file, 's3-etl-project', 'enterprise/enterprise.csv')
glue_client = boto3.client('glue',region_name='us-east-1')
response = glue_client.create_database(
    CatalogId='string',
    DatabaseInput={
        'Name': 'etl-project',})
print(response)