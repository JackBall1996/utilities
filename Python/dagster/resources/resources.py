from dagster import resource
import boto3


@resource
def s3_resource(_):
    """
    Dagster resource that provides a boto3 S3 client using the environment's AWS credentials.
    Assumes role is already assumed (e.g., via AWS CLI, EC2 metadata, or exported environment variables).
    """
    session = boto3.Session()  # Uses environment/EC2 role credentials by default
    return session.client("s3")
