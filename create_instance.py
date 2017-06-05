import boto3
ec2 = boto3.resource('ec2')
ec2.create_instances(ImageId='ami-c58c1dd3', MinCount=1, MaxCount=1)