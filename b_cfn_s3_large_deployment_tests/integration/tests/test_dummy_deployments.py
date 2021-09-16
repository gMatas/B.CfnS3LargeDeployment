import logging
import os

from b_aws_testing_framework.credentials import Credentials

from b_cfn_s3_large_deployment_tests.integration import ROOT_PATH
from b_cfn_s3_large_deployment_tests.integration.infrastructure import Infrastructure

logger = logging.getLogger(__name__)


def test_small_deployment_deployed() -> None:
    deployment_output_keys = Infrastructure.SMALL_DEPLOYMENT_OUTPUT_KEYS
    destination_bucket_name = Infrastructure.get_output(deployment_output_keys.destination_bucket_name)
    destination_bucket_key_prefix = Infrastructure.get_output(deployment_output_keys.destination_bucket_key_prefix)

    dummy_deployments_dirpath = os.path.join(ROOT_PATH, 'dummy_deployments')

    # Require only files marked with '.deploy' suffix to be deployed.
    required_files = {
        filename
        for filename in os.listdir(os.path.join(dummy_deployments_dirpath, deployment_output_keys.source_name))
        if filename.endswith('.deploy')
    }

    s3_resource = Credentials().boto_session.resource('s3')
    bucket = s3_resource.Bucket(destination_bucket_name)
    deployed_files = {
        os.path.basename(obj.key)
        for obj in bucket.objects.filter(Prefix=destination_bucket_key_prefix)
    }

    missing_files = required_files.difference(deployed_files)
    assert not missing_files, f'Missing files from deployment: {list(missing_files)}'


def test_large_deployment_deployed() -> None:
    deployment_output_keys = Infrastructure.LARGE_DEPLOYMENT_OUTPUT_KEYS
    destination_bucket_name = Infrastructure.get_output(deployment_output_keys.destination_bucket_name)
    destination_bucket_key_prefix = Infrastructure.get_output(deployment_output_keys.destination_bucket_key_prefix)

    dummy_deployments_dirpath = os.path.join(ROOT_PATH, 'dummy_deployments')

    # Require only files marked with '.deploy' suffix to be deployed.
    required_files = {
        filename
        for filename in os.listdir(os.path.join(dummy_deployments_dirpath, deployment_output_keys.source_name))
        if filename.endswith('.deploy')
    }

    s3_resource = Credentials().boto_session.resource('s3')
    bucket = s3_resource.Bucket(destination_bucket_name)
    deployed_files = {
        os.path.basename(obj.key)
        for obj in bucket.objects.filter(Prefix=destination_bucket_key_prefix)
    }

    missing_files = required_files.difference(deployed_files)
    assert not missing_files, f'Missing files from deployment: {list(missing_files)}'
