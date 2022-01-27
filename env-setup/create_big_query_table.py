""" This template creates a BigQuery table. """


def generate_config(context):
    """ Entry point for the deployment resources. """

    properties = context.properties
    name = properties.get('name', context.env['name'])
    project_id = properties.get('project', context.env['project'])

    properties = {
        'tableReference':
            {
                'tableId': name,
                'datasetId': context.properties['datasetId'],
                'projectId': project_id
            },
        'datasetId': context.properties['datasetId'],
        'projectId': project_id,
    }

    optional_properties = [
        'description',
        'friendlyName',
        'expirationTime',
        'schema',
        'timePartitioning',
        'externalDataConfiguration',
        'view'
    ]

    for prop in optional_properties:
        if prop in context.properties:
            if prop == 'schema':
                properties[prop] = {'fields': context.properties[prop]}
            else:
                properties[prop] = context.properties[prop]

    resources = [
        {
            # https://cloud.google.com/bigquery/docs/reference/rest/v2/tables
            'type': 'gcp-types/bigquery-v2:tables',
            'name': context.env['name'],
            'properties': properties
        }
    ]

    if 'dependsOn' in context.properties:
        resources[0]['metadata'] = {'dependsOn': context.properties['dependsOn']}

    outputs = [
        {
            'name': 'selfLink',
            'value': '$(ref.{}.selfLink)'.format(context.env['name'])
        },
        {
            'name': 'etag',
            'value': '$(ref.{}.etag)'.format(context.env['name'])
        },
        {
            'name': 'creationTime',
            'value': '$(ref.{}.creationTime)'.format(context.env['name'])
        },
        {
            'name': 'lastModifiedTime',
            'value': '$(ref.{}.lastModifiedTime)'.format(context.env['name'])
        },
        {
            'name': 'location',
            'value': '$(ref.{}.location)'.format(context.env['name'])
        },
        {
            'name': 'numBytes',
            'value': '$(ref.{}.numBytes)'.format(context.env['name'])
        },
        {
            'name': 'numLongTermBytes',
            'value': '$(ref.{}.numLongTermBytes)'.format(context.env['name'])
        },
        {
            'name': 'numRows',
            'value': '$(ref.{}.numRows)'.format(context.env['name'])
        },
        {
            'name': 'type',
            'value': '$(ref.{}.type)'.format(context.env['name'])
        }
    ]

    return {'resources': resources, 'outputs': outputs}