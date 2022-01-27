import os

def temp_trigger_etl_flow(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    dataflow_exec(event, context)
    print(f"Processing file: {event['name']}.")


def dataflow_exec(file, context):
    from googleapiclient.discovery import build
    # replace with your projectID
    project = os.environ.get('PROJECT_NM')
    title = os.environ.get('ETL_NM')
    job = project + title + str(file['timeCreated'])
    # path of the dataflow template on google storage bucket
    #template = "gs://gcp_etl_project/dataflow_templates/product_category/template/GCP_Product_Category_ETL"
    template=os.environ.get('TEMPLATE_LOC')

    inputFile = "gs://" + str(file['bucket']) + "/" + str(file['name'])
    # user defined parameters to pass to the dataflow pipeline job
    parameters = {
        'input': inputFile,
        'project_nm': project,
    }
    # tempLocation is the path on GCS to store temp files generated during the dataflow job
    environment = {
        'tempLocation': os.environ.get('TEMP_LOC') } #'gs://gcp_olist_etl_project/gcp_etl_project/dataflow_templates/product_category/temp'}

    service = build('dataflow', 'v1b3', cache_discovery=False)
    # below API is used when we want to pass the location of the dataflow job
    request = service.projects().locations().templates().launch(
        projectId=project,
        gcsPath=template,
        location=os.environ.get('LOCATION'),
        body={
            'jobName': job,
            'parameters': parameters,
            'environment': environment
        },
    )
    response = request.execute()
    print(str(response))

#gcloud config set project PROJECT_ID