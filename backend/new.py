import boto3, os
c = boto3.client(
  "rekognition",
  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
  region_name="us-east-1"
)
print(c.list_collections())
