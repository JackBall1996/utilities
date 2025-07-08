from dagster import asset, op, AssetExecutionContext, AssetIn, OpExecutionContext
from sqlalchemy.exc import SQLAlchemyError
import connection_manager as cm
from read_yaml import open_yaml
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Initialize a global context
global_context = None

# Function to set the context globally
def set_context(context: AssetExecutionContext):
    global global_context
    global_context = context

# Operator to log initial activity
@op 
def log_activity_start(yaml_file_name):
    """_summary_
    logs the pipeline start
    """
    # yaml assign variables 
    project_name = open_yaml(yaml_file_name,'project_name')
    project_description = open_yaml(yaml_file_name,'project_description')
    project_main_contact = open_yaml(yaml_file_name,'project_main_contact')
    project_sponsor = open_yaml(yaml_file_name,'project_sponsor')
    project_email = open_yaml(yaml_file_name,'project_email')
    project_create_date = open_yaml(yaml_file_name,'project_create_date')
    environment = open_yaml(yaml_file_name,'env')
    process_name = 'main process'
    status = 'processing'
    source_datasets = ''
    target_database = ''
    start_time = datetime.now()
    mailing_list = ''
    
    sql_engine = cm.create_db_engine('SQLCLUSCOLDEV19\DEV19','AM_Dev')   
    
    session = sessionmaker(bind=sql_engine)
    session = session()  
    
    try:
        global_context.log.info(f"Logging start of process '{project_name}' at {start_time}")
        session.execute(
            """
            INSERT INTO [dbo].[am_pipeline_log]
                                    ([project_name]
                                    ,[project_description]
                                    ,[project_main_contact]
                                    ,[project_sponsor]
                                    ,[project_email]
                                    ,[project_create_date]
                                    ,[environment]
                                    ,[process_name]
                                    ,[status]
                                    ,[source_datasets]
                                    ,[target_database]
                                    ,[time]
                                    ,[mailing_list])
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (project_name, project_description, project_main_contact, project_sponsor, project_email, project_create_date, environment, process_name, status, source_datasets, target_database, start_time, mailing_list)
            )
        session.commit()
    except SQLAlchemyError as e:
        global_context.log.info(f"Error logging activity: {e}")
    finally:
        session.close()
        sql_engine.dispose()
        
# Ingest CSV to Database OP
@op 
def ingest_csv_file(server, database, file_path, table_name):
    """_summary_
    ingests csv file
    """
    df = pd.read_csv(file_path, on_bad_lines='skip')
    
    sql_engine = cm.create_db_engine(server,database) 
    
    session = sessionmaker(bind=sql_engine)
    session = session() 
    
    try: 
        schema = table_name.split('.')[0]
        table_name = table_name.split('.')[1]
        df.to_sql(table_name, con = sql_engine, if_exists = 'replace')
        session.commit()
    except Exception as e:
        session.rollback()
        global_context.log.info(f"Error occurred: {e}")
    finally:
        session.close()
        sql_engine.dispose()
    

# Create dynamic CSV asset  
def create_dynamic_asset_csv(asset_name, server, database, file_path, table_name, dependencies):
    # Programmatically construct the ins dictionary
    ins_dict = {
        'log_initial_activity': AssetIn()
    }
    @asset(name=asset_name,
        ins=ins_dict
    )
    def dynamic_asset(context: AssetExecutionContext, log_initial_activity: str):
        """
        asset description
        """
        set_context(context)
        log_message = f"Loading {file_path} to database {database} on {server}"
        context.log.info(log_message)        
        ingest_csv_file(server = server, database = database, file_path = file_path, table_name = table_name)
        log_message = f"Successfully loaded {file_path} to database {database} on {server}"
        context.log.info(log_message)    
    return dynamic_asset

# Operator to log initial activity
@op 
def log_activity_end(yaml_file_name):
    """_summary_
    logs the pipeline end
    """
    # yaml assign variables 
    project_name = open_yaml(yaml_file_name,'project_name')
    
    sql_engine = cm.create_db_engine('SQLCLUSCOLDEV19\DEV19','AM_Dev')    
    
    session = sessionmaker(bind=sql_engine)
    session = session()  
    
    try:
        end_time = datetime.now()
        global_context.log.info(f"Logging completion of process '{project_name}' at {end_time}")
        session.execute(
            """
            UPDATE [dbo].[am_pipeline_log]
            SET status = %s, end_time = %s
            WHERE project_name = %s AND status = %s
            """,
            ('COMPLETED', end_time, project_name, 'processing')
        )
        session.commit()
    except SQLAlchemyError as e:
        global_context.log.info(f"Error logging activity completion: {e}")
    finally:
        session.close()
        sql_engine.dispose()