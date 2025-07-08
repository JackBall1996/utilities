import yaml
import os

os.chdir('C:\\Users\Jack.Ball\OneDrive - UK Health Security Agency\Documents\Work\Repos\jackball\dagster')  # Provide the new path here

# Load the YAML file
def open_yaml(file_name, value):
    with open(file_name, "r") as file:
        data = yaml.safe_load(file)

        pipeline_data = {
                'project_name':data["Project"].get('projectdescription', []).get('name'),
                'environment':data["Project"].get('projectdescription', []).get('env'),
                'project_description':data["Project"].get('projectdescription', []).get('description'),
                'project_main_contact':data["Project"].get('projectdescription', []).get('main_contact'),
                'project_sponsor':data["Project"].get('projectdescription', []).get('project_sponsor'),
                'project_email':data["Project"].get('projectdescription', []).get('project_email'),
                'project_create_date':data["Project"].get('projectdescription', []).get('create_date'),
                'source_datasets': data["Project"].get("datasets", []),
                'target_database':data["Project"].get("target", []),
                'mailing_list': data["Project"].get('projectdescription', []).get('mailing_list'),
                'env': data["Project"].get('projectdescription', []).get('env'),
                'schedule': data["Project"].get('projectdescription', []).get('schedule'),
                'target': data["Project"].get("target", []),
            }
    return pipeline_data.get(value)
        