import boto3
from botocore.exceptions import ClientError
import json


def get_secret():

    secret_name = "guardian_key"
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    decoded_secret = json.loads(secret)

    return decoded_secret["gnews_key"]

the_key = get_secret()


