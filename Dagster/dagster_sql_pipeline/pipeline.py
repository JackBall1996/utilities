from dagster import asset, AssetExecutionContext, Definitions, define_asset_job, define_asset_job, AssetSelection, ScheduleDefinition
from read_yaml import open_yaml
import operators

# Set variables
yaml = open_yaml("test.yml",'target_database')    
server = yaml[0].get('server')
database = yaml[0].get('database_name')

yaml = list(open_yaml("test.yml",'source_datasets'))
i = 1
all_assets = []

#Asset to log initial activity
@asset 
def log_initial_activity(context: AssetExecutionContext) -> str:
    log_message = "Started processing test.yml"
    operators.set_context(context)
    operators.log_activity_start("test.yml")
    context.log.info(log_message)
    return log_message
    
#Create ingest csv assets   
for dataset in yaml:
    if dataset['type'] == 'file':
        for file in dataset['files']:
            file_path = file.get('file_path')[0]
            table_name = file.get('table_name') 
            asset_name = dataset['dataset'] + str(i)
            
            dynamic_asset = operators.create_dynamic_asset_csv(
                asset_name=asset_name, 
                server=server, 
                database=database, 
                file_path=file_path, 
                table_name=table_name,
                dependencies=['log_initial_activity']
            )
            
            all_assets.append(dynamic_asset)    
            
            i += 1
    if dataset['type'] == 'sql_query':
        print('sql query')
        
#Asset to log activity end
@asset(deps=all_assets)
def log_end_activity(context: AssetExecutionContext) -> str:
    log_message = "Finished processing test.yml"
    operators.set_context(context)
    operators.log_activity_end("test.yml")
    context.log.info(log_message)
    return log_message    

#Register assets
all_assets.append(log_initial_activity)
all_assets.append(log_end_activity)

# Register the assets with Definitions
project_name = open_yaml("test.yml",'project_name')    
project_schedule = open_yaml("test.yml",'schedule')    

defs = Definitions(
    assets=all_assets,
    jobs = [
        define_asset_job(
            name=project_name + '_job',
            selection=AssetSelection.all()
        )
    ],
    schedules=[
        ScheduleDefinition(
            name = project_name + '_schedule',
            job_name = project_name + '_job',
            cron_schedule = project_schedule
        )
    ]
    
)