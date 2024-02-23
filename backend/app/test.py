import sys

import boto3

# Initialize the AWS clients
lambda_client = boto3.client(
    'lambda', region_name='ap-northeast-1',
    aws_access_key_id='AKIAWDF4LM2U4M26PTN6',
    aws_secret_access_key='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',
)


def create_layer_version(layer_name, _s3_buket, _s3_key, _compatible_runtimes):
    """Create a new layer version."""
    response = lambda_client.publish_layer_version(
        LayerName=layer_name,
        Content={
            'S3Bucket': _s3_buket,
            'S3Key': _s3_key
        },
        CompatibleRuntimes=_compatible_runtimes
    )
    return response['LayerVersionArn']


def check_layer_version_exists(layer_name, version):
    """Check if a layer version exists."""
    try:
        lambda_client.get_layer_version(
            LayerName=layer_name,
            VersionNumber=version
        )
        return True
    except lambda_client.exceptions.ResourceNotFoundException:
        return False


def check_layer_exists(layer_name):
    """Check if a layer exists."""
    try:
        lambda_client.get_layer_version(
            LayerName=layer_name,
        )
        return True
    except lambda_client.exceptions.ResourceNotFoundException:
        return False


def get_last_version(layer_name):
    """Check if a layer exists."""
    try:
        response = lambda_client.list_layer_versions(
            LayerName=layer_name,
        )
        if not response['LayerVersions']:
            return False
        return response['LayerVersions'][0]['Version']
    except lambda_client.exceptions.ResourceNotFoundException:
        return False


def update_layer_for_lambda_function(_layer_arn, _function_name):
    """Update a Lambda function to use a new layer version."""
    lambda_client.update_function_configuration(
        FunctionName=_function_name,
        Layers=[
            _layer_arn
        ]
    )


if __name__ == '__main__':
    # get values from input parameters
    s3_buket = sys.argv[1]
    env = sys.argv[2]
    function_name = sys.argv[3]
    print(function_name)
    s3_key = 'python.zip'

    # Set the layer parameters
    lambda_layer_name = f'tbyb-lambda-layer-{env}'
    compatible_runtimes = ['python3.9']
    last_version = get_last_version(lambda_layer_name)

    layer_arn = create_layer_version(
        lambda_layer_name, s3_buket, s3_key, compatible_runtimes
    )

    update_layer_for_lambda_function(_layer_arn=layer_arn, _function_name=function_name)
