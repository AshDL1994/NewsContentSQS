import json
import boto3
import pytest
from botocore.exceptions import ClientError
from moto import mock_aws
from src.utils.key import get_secret  

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    boto3.setup_default_session()

@mock_aws
def test_get_secret_success(aws_credentials):
    """Test successful retrieval of the secret."""
    secret_name = "guardian_key"
    region_name = "eu-west-2"
    secret_value = {"gnews_key": "test-api-key"}

    client = boto3.client("secretsmanager", region_name=region_name)

    client.create_secret(
        Name=secret_name,
        SecretString=json.dumps(secret_value)
    )

    assert get_secret() == "test-api-key"


@mock_aws
def test_get_secret_not_found(aws_credentials):
    """Test handling of secret not found error."""
    with pytest.raises(ClientError) as e:
        get_secret()
    
    assert e.value.response["Error"]["Code"] == "ResourceNotFoundException"


