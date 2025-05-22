import boto3
import botocore

# Mapping from region to access logging bucket name
REGION_LOG_BUCKET_MAP = {
    'us-east-1': 's3-access-logs-use1',
    'us-west-2': 's3-access-logs-usw2',
    'eu-west-1': 's3-access-logs-euw1',
    # Add more region mappings as needed
}

# Get the region of an S3 bucket
def get_bucket_region(bucket_name):
    s3 = boto3.client('s3')
    try:
        response = s3.get_bucket_location(Bucket=bucket_name)
        region = response.get('LocationConstraint') or 'us-east-1'
        return region
    except botocore.exceptions.ClientError as e:
        print(f"[ERROR] Failed to get region for {bucket_name}: {e}")
        return None

# Enable access logging on the bucket
def enable_access_logging(bucket_name, log_bucket, log_prefix):
    s3 = boto3.client('s3')
    try:
        s3.put_bucket_logging(
            Bucket=bucket_name,
            BucketLoggingStatus={
                'LoggingEnabled': {
                    'TargetBucket': log_bucket,
                    'TargetPrefix': f"{log_prefix}/{bucket_name}/"
                }
            }
        )
        print(f"[OK] Enabled logging on {bucket_name} → {log_bucket}/{log_prefix}/{bucket_name}/")
    except botocore.exceptions.ClientError as e:
        print(f"[ERROR] Failed to enable logging on {bucket_name}: {e}")

def main():
    bucket_name = input("Enter the name of the S3 bucket to enable logging on: ").strip()
    if not bucket_name:
        print("Bucket name cannot be empty.")
        return

    region = get_bucket_region(bucket_name)
    if not region:
        return

    log_bucket = REGION_LOG_BUCKET_MAP.get(region)
    if not log_bucket:
        print(f"[SKIP] No logging bucket defined for region '{region}'.")
        return

    log_prefix = "<TO_BE_DEFINED>"  # You can later replace this with a user prompt or logic
    enable_access_logging(bucket_name, log_bucket, log_prefix)

if __name__ == "__main__":
    main()