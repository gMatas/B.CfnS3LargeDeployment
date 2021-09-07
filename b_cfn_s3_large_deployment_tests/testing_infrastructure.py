import os
from importlib.resources import path

from aws_cdk.aws_s3 import Bucket
from aws_cdk.core import Stack, Construct, RemovalPolicy

import b_cfn_s3_large_deployment_tests
from b_cfn_s3_large_deployment.deployment_props import DeploymentProps
from b_cfn_s3_large_deployment.deployment_source import AssetDeploymentSource
from b_cfn_s3_large_deployment.resource import S3LargeDeploymentResource


class TestingInfrastructure(Stack):
    def __init__(self, scope: Construct):
        super().__init__(
            scope=scope,
            id=f'Testing-LargeDeployment-Stack',
            stack_name=f'Testing-LargeDeployment-Stack'
        )

        with path(b_cfn_s3_large_deployment_tests, 'small_dummy_deployment.zip') as deployment_path:
            small_dummy_deployment_source = AssetDeploymentSource(path=os.path.join(deployment_path))

        S3LargeDeploymentResource(
            scope=self,
            name=f'TestingLargeDeployment',
            props=DeploymentProps(
                sources=[
                    small_dummy_deployment_source
                ],
                destination_bucket=Bucket(
                    scope=self,
                    id=f'testing-large-deployment-bucket',
                    auto_delete_objects=True,
                    removal_policy=RemovalPolicy.DESTROY,
                )
            )
        )
