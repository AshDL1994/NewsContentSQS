import boto3
import pytest
from moto import mock_aws
from botocore.exceptions import ClientError
from src.utils.send_messages import create_queue_return_url, list_all_queues, send_message_to_queue

@mock_aws
def test_create_queue_success():
    """Test that the function successfully creates a queue and returns its URL."""
    sqs = boto3.client("sqs", region_name="eu-west-2")
    
    queue_name = "test-queue"
    queue_url = create_queue_return_url(queue_name)

    response = sqs.list_queues()
    assert queue_url in response.get("QueueUrls", [])

@mock_aws
def test_create_queue_failure():
    """Test handling of errors during queue creation."""
    with pytest.raises(Exception):
        create_queue_return_url("a" * 81)  # AWS limits queue names to 80 chars

@mock_aws
def test_list_all_queues_with_queues():
    """Test that list_all_queues returns correct queue names when SQS queues exist."""
    client = boto3.client("sqs", region_name="eu-west-2")
    
    client.create_queue(QueueName="TestQueue1")
    client.create_queue(QueueName="TestQueue2")

    queues = list_all_queues()
    
    assert sorted(queues) == ["TestQueue1", "TestQueue2"]        

@mock_aws
def test_list_all_queues_no_queues():
    """Test that list_all_queues returns an empty list when no queues exist."""
    client = boto3.client("sqs", region_name="eu-west-2")

    queues = list_all_queues()

    assert queues == "Something went wrong. Please check if you have queues available."    


@mock_aws
def test_send_message_fail():
    
    sqs_client = boto3.client('sqs', region_name='us-east-1')

    sqs_client.create_queue(QueueName='test-queue')
    
    queue_url = sqs_client.get_queue_url(QueueName='test-queue')['QueueUrl']
    
    message_body = "Hello, World!"
    
    response = send_message_to_queue(queue_url, message_body)
    
    assert "Failed to send message. Please check the queue and try again." in response

    