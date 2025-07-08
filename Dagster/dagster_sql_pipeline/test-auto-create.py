from typing import List
from dagster import asset, AssetExecutionContext, AssetIn, Definitions, define_asset_job, AssetSelection, ScheduleDefinition
import yaml
import os

os.chdir('C:\\Users\Jack.Ball\OneDrive - UK Health Security Agency\Documents\Work\Repos\jackball\dagster')  # Provide the new path her

# Load the YAML file
with open("test.yml", "r") as file:
    data = yaml.safe_load(file)
    
    datasets = data["Project"].get("datasets", [])
    env = data["Project"].get('projectdescription', []).get('env')
    schedule = data["Project"].get('projectdescription', []).get('schedule')
    target = data["Project"].get("target", [])

    pipeline_data = {
            'project_name':data["Project"].get('projectdescription', []).get('name'),
            'environment':data["Project"].get('projectdescription', []).get('env'),
            'project_description':data["Project"].get('projectdescription', []).get('description'),
            'project_main_contact':data["Project"].get('projectdescription', []).get('main_contact'),
            'project_sponsor':data["Project"].get('projectdescription', []).get('project_sponsor'),
            'project_email':data["Project"].get('projectdescription', []).get('project_email'),
            'project_create_date':data["Project"].get('projectdescription', []).get('create_date'),
            'source_datasets': data["Project"].get("datasets", []),
            'target_database':data["Project"].get("target", []) ,
            'mailing_list': data["Project"].get('projectdescription', []).get('mailing_list'),
        }
    
@asset
def initial_logs(context: AssetExecutionContext):
    """
    test description
    """
    context.log.info(f"initial log")   
        
#print(pipeline_data["target_database"][0].get("server"))

def create_dynamic_asset(asset_name,source_dataset):
    @asset(name=asset_name,deps=[initial_logs])
    def dynamic_asset(context: AssetExecutionContext):
        """
        asset description
        """
        data = source_dataset.get("type")
        context.log.info(f"dataset type is: {data}")
        return data
    return dynamic_asset
        
all_assets = []

for source_dataset in pipeline_data["source_datasets"]:
    asset_name = source_dataset.get("dataset")
    
    dynamic_asset = create_dynamic_asset(asset_name=asset_name, source_dataset=source_dataset)
    all_assets.append(dynamic_asset)  # Append the actual asset, not just the name
    
#print(all_assets)

@asset(deps=all_assets)
def exit_logs(context: AssetExecutionContext):
    """
    exit description
    """
    context.log.info(f"exit log")   

all_assets.append(initial_logs)
all_assets.append(exit_logs)

# Register the assets with Definitions
defs = Definitions(
    assets=all_assets
)
    
    # print(source_dataset.get("type"))
    # print(source_dataset.get("files"))
    # if source_dataset.get("type") == "file":
    #     print(source_dataset.get("files")[0].get("file_path"))