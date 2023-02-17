import boto3
import pytest

@pytest.fixture(scope='module')
def s3_client():
    # Set up an S3 client
    client = boto3.client('s3')
    return client

def test_create_s3_bucket(s3_client):
    # Define bucket parameters
    bucket_name = 'my-test-bucket'
    region = 'us-west-2'

    # Create the bucket
    s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': region
        }
    )

    # Check if the bucket exists
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    assert bucket_name in buckets

    # Delete the bucket
    s3_client.delete_bucket(Bucket=bucket_name)
