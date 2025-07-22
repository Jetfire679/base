import boto3
import time
import json
from datetime import datetime
import os

# ---- CONFIG ----
log_group = "/aws/route53/query"
region = "us-east-1"
bucket_name = "your-bucket-name"
s3_key_prefix = "route53/query-results"
query_string = """
fields @timestamp, queryName = parse_json(@message).queryName 
| filter queryName like /(^|\\.)example\\.com\\./
"""

# ---- TIME RANGE ----
start_time = int(datetime(2025, 7, 21, 0, 0).timestamp())
end_time = int(datetime(2025, 7, 21, 23, 59, 59).timestamp())

# ---- AWS CLIENTS ----
logs = boto3.client("logs", region_name=region)
s3 = boto3.client("s3", region_name=region)

# ---- START QUERY ----
response = logs.start_query(
    logGroupName=log_group,
    startTime=start_time,
    endTime=end_time,
    queryString=query_string
)
query_id = response["queryId"]
print(f"Started query: {query_id}")

# ---- WAIT FOR RESULTS ----
status = "Running"
while status in ["Running", "Scheduled"]:
    time.sleep(2)
    result = logs.get_query_results(queryId=query_id)
    status = result["status"]
    print(f"Query status: {status}...")

# ---- SAVE TO FILE ----
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
filename = f"query-results-{timestamp}.json"
with open(filename, "w") as f:
    json.dump(result, f, indent=2)

print(f"Saved results to {filename}")

# ---- UPLOAD TO S3 ----
s3_key = f"{s3_key_prefix}/{filename}"
s3.upload_file(filename, bucket_name, s3_key)
print(f"Uploaded to s3://{bucket_name}/{s3_key}")

# ---- CLEANUP (optional) ----
os.remove(filename)
print("Done.")