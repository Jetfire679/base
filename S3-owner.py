import boto3
import datetime

# Replace with your bucket name
bucket_name = "your-bucket-name"

# Create CloudTrail client
client = boto3.client('cloudtrail')

# Define the time window to search in (e.g., past 90 days)
end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(days=90)

# Lookup events
response = client.lookup_events(
    LookupAttributes=[
        {
            'AttributeKey': 'EventName',
            'AttributeValue': 'CreateBucket'
        },
    ],
    StartTime=start_time,
    EndTime=end_time,
    MaxResults=50
)

# Filter the events to match the specific bucket
for event in response['Events']:
    if bucket_name in event['CloudTrailEvent']:
        import json
        event_detail = json.loads(event['CloudTrailEvent'])
        user_identity = event_detail['userIdentity']
        print(f"Bucket was created by: {user_identity.get('arn', 'Unknown')}")
        break
else:
    print(f"No CreateBucket event found for bucket: {bucket_name}")


import boto3

cf = boto3.client('cloudformation')

def find_bucket_in_stacks(bucket_name):
    stacks = cf.list_stacks(StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE'])['StackSummaries']
    for stack in stacks:
        resources = cf.list_stack_resources(StackName=stack['StackName'])['StackResourceSummaries']
        for res in resources:
            if res['ResourceType'] == 'AWS::S3::Bucket' and res['PhysicalResourceId'] == bucket_name:
                return stack['StackName']
    return None

bucket_name = "your-bucket-name"
stack_name = find_bucket_in_stacks(bucket_name)
if stack_name:
    print(f"Bucket was created by stack: {stack_name}")
else:
    print("No CloudFormation stack found for this bucket.")
