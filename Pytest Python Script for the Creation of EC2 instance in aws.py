import boto3
import pytest

@pytest.fixture(scope='module')
def ec2_client():
    # Set up an EC2 client
    client = boto3.client('ec2')
    return client

def test_create_ec2_instance(ec2_client):
    # Define instance parameters
    image_id = 'ami-0c55b159cbfafe1f0' # Amazon Linux 2 AMI (HVM), SSD Volume Type
    instance_type = 't2.micro'
    key_name = 'my-key-pair'
    security_group_ids = ['sg-1234567890abcdef0']

    # Launch the instance
    response = ec2_client.run_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        KeyName=key_name,
        SecurityGroupIds=security_group_ids,
        MinCount=1,
        MaxCount=1
    )

    # Check if the instance was launched successfully
    instance_id = response['Instances'][0]['InstanceId']
    waiter = ec2_client.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    instance = ec2_client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
    assert instance['State']['Name'] == 'running'

    # Terminate the instance
    ec2_client.terminate_instances(InstanceIds=[instance_id])