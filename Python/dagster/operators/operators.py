import pandas as pd
from dagster import op, In, Out, String, Nothing, Field
from io import StringIO
from Python.functionality.transformations import add_timestamp_column


@op(
    required_resource_keys={"s3"},
    out=Out(pd.DataFrame),
    config_schema={"bucket": String, "key": String},
)
def read_csv_from_s3(context) -> pd.DataFrame:
    """
    Downloads a CSV file from an S3 bucket and loads it into a Pandas DataFrame.

    This op requires an S3 resource configured in the Dagster context. It reads the
    object specified by the `bucket` and `key` configuration fields, decodes it as UTF-8,
    and parses it into a Pandas DataFrame.

    Config:
        bucket (str): Name of the S3 bucket.
        key (str): Key (path) to the CSV object within the S3 bucket.

    Returns:
        pd.DataFrame: The loaded DataFrame from the CSV file.
    """
    bucket = context.op_config["bucket"]
    key = context.op_config["key"]

    s3_client = context.resources.s3

    context.log.info(f"Downloading s3://{bucket}/{key}")

    response = s3_client.get_object(Bucket=bucket, Key=key)
    csv_data = response["Body"].read().decode("utf-8")

    df = pd.read_csv(StringIO(csv_data))
    context.log.info(
        f"Loaded DataFrame with {len(df)} rows and {len(df.columns)} columns"
    )

    return df


@op(
    ins={"df": In(pd.DataFrame)},
    out=Out(Nothing),
    required_resource_keys={"s3"},
    config_schema={"bucket": String, "key": String},
)
def write_csv_to_s3(context, df: pd.DataFrame) -> None:
    """
    Writes a Pandas DataFrame to a CSV file and uploads it to an S3 bucket.

    This op converts the input DataFrame to a CSV string and uploads it to the specified
    S3 location using the configured S3 resource.

    Config:
        bucket (str): Name of the destination S3 bucket.
        key (str): Key (path) within the bucket to store the CSV file.

    Args:
        context (OpExecutionContext): Dagster context containing configuration and resources.
        df (pd.DataFrame): DataFrame to serialize and upload to S3.
    """

    bucket = context.op_config["bucket"]
    key = context.op_config["key"]

    context.log.info(f"Writing DataFrame to s3://{bucket}/{key}")

    # Convert DataFrame to CSV in memory
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # Upload to S3 using the injected boto3 S3 client
    s3_client = context.resources.s3
    context.log.info(f"{s3_client=}")
    s3_client.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())

    context.log.info("Upload Completed")


@op(
    ins={"df": In(pd.DataFrame)},
    out=Out(pd.DataFrame),
    config_schema={
        "timestamp_column_name": Field(
            String, is_required=False, default_value="ingest_timestamp"
        )
    },
)
def op_add_timestamp_column(context, df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a column with the current timestamp to the input DataFrame.

    This op uses the `add_timestamp_column` transformation to add a new column
    with the current datetime to the DataFrame. The name of the column can be
    customized via configuration.

    Config:
        timestamp_column_name (str, optional): Name of the column to add. Defaults to 'ingest_timestamp'.

    Args:
        context (OpExecutionContext): Dagster context containing configuration.
        df (pd.DataFrame): Input DataFrame to augment with a timestamp column.

    Returns:
        pd.DataFrame: DataFrame with the added timestamp column.
    """
    timestamp_column_name = context.op_config.get("timestamp_column_name")

    context.log.info(f"Adding current datetime column: '{timestamp_column_name}'")

    df = add_timestamp_column(df=df, timestamp_column_name=timestamp_column_name)

    return df
