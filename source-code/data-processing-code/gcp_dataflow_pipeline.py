import argparse
import logging

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import datetime

class OlistDatasetOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        # Use add_value_provider_argument for arguments to be templatable
        # Use add_argument as usual for non-templatable arguments
        parser.add_value_provider_argument(
            '--input',
            default='gs://dataflow-samples/shakespeare/kinglear.txt',
            help='Path of the file to read from')
        parser.add_value_provider_argument(
            '--project_nm',
            default='gcp-learning-333002',
            help='project id')


if __name__ == '__main__':
    #datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
    logging.getLogger().setLevel(logging.INFO)
    # Create the Pipeline with remaining arguments.
    beam_options = PipelineOptions()
    #pipeline = beam.Pipeline(options=beam_options)

    with beam.Pipeline(options=beam_options) as p:
        olist_dataset_options = beam_options.view_as(OlistDatasetOptions)

        SCHEMA = 'order_id:String,customer_id:STRING,order_status:INTEGER,order_purchase_timestamp:DATETIME,' \
                 'order_approved_at:DATETIME,order_delivered_carrier_date:DATETIME,' \
                 'order_delivered_customer_date:DATETIME,order_estimated_delivery_date:DATETIME'
        (p | 'Read files' >> beam.io.ReadFromText(olist_dataset_options.input, skip_header_lines=1)
         | 'Split' >> beam.Map(lambda x: x.split(','))
         | 'Filter Blank Row' >> beam.Filter(lambda x: x[0] != '' and x[1] != '')
         | 'Making product Dict Map' >> beam.Map(
                    lambda x: {'order_id': x[0], 'customer_id': x[1],'order_status':int(x[2]),'order_purchase_timestamp':datetime.strptime(x[3], "%y-%m-%d %H:%M:%S"),
                               'order_approved_at':datetime.strptime(x[4], "%y-%m-%d %H:%M:%S"),'order_delivered_carrier_date':datetime.strptime(x[5], "%y-%m-%d %H:%M:%S"),
                               'order_delivered_customer_date':datetime.strptime(x[6], "%y-%m-%d %H:%M:%S"),'order_estimated_delivery_date':datetime.strptime(x[7], "%y-%m-%d %H:%M:%S")
                               })
         | 'Write ProductCat BigQuery' >> beam.io.WriteToBigQuery(table=olist_dataset_options.project_nm+':olist_demo_dataset.olist_order',
                                                                  schema=SCHEMA,
                                                                  write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
         )
