from dagster import op, job
import os
from dagster import sensor, RunRequest

WATCHED_DIRECTORY = "/path/to/watched_directory"

@op
def process_file_op(context, file_name: str):
    context.log.info(f"Processing file: {file_name}")

@job
def process_file_job():
    process_file_op()
    
@sensor(job=process_file_job, minimum_interval_seconds=300)  # 5 minutes, default is 30 seconds
def my_file_sensor(context):
    # Check for files in the watched directory
    for file_name in os.listdir(WATCHED_DIRECTORY):
        if file_name.endswith(".csv"):  # Only process CSV files
            context.log.info(f"Found new file: {file_name}")
            # Trigger the job and pass the file name as an input
            yield RunRequest(
                run_key=file_name,  # Prevents multiple executions for the same file
                run_config={
                    "ops": {
                        "process_file_op": {
                            "inputs": {
                                "file_name": file_name
                            }
                        }
                    }
                }
            )