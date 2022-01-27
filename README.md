# CI-CD-Python-Order-ETL

use below command to create resources for order pipeline

gcloud deployment-manager deployments create ci-cd-python-order-etl --config batch_pipeline_infra_setup.yaml 

use below for delete resources 
gcloud deployment-manager deployments delete ci-cd-python-order-etl-v1