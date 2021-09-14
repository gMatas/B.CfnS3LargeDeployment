import os
from importlib.resources import path

from aws_cdk.aws_ec2 import Vpc, SubnetConfiguration, SubnetType, SubnetSelection
from aws_cdk.aws_s3 import Bucket
from aws_cdk.core import Construct, RemovalPolicy
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack

import b_cfn_s3_large_deployment_tests
from b_cfn_s3_large_deployment.deployment_props import DeploymentProps
from b_cfn_s3_large_deployment.deployment_source import AssetDeploymentSource
from b_cfn_s3_large_deployment.resource import S3LargeDeploymentResource


class Infrastructure(TestingStack):
    def __init__(self, scope: Construct):
        super().__init__(scope=scope)

        testing_vpc = Vpc(
            scope=self,
            id=f'{self.global_prefix()}LargeDeploymentVpc',
            max_azs=1,
            nat_gateways=1,
            subnet_configuration=[
                SubnetConfiguration(
                    name=f'{self.global_prefix()}LargeDeploymentVpcPublicSubnet',
                    subnet_type=SubnetType.PUBLIC,
                    cidr_mask=22
                ),
                SubnetConfiguration(
                    name=f'{self.global_prefix()}LargeDeploymentVpcPrivateSubnet',
                    subnet_type=SubnetType.PRIVATE,
                    cidr_mask=22
                )
            ]
        )

        testing_destination_bucket = Bucket(
            scope=self,
            id=f'{self.global_prefix()}-large-deployment-bucket',
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY
        )

        with path(b_cfn_s3_large_deployment_tests, 'dummy_deployments') as deployment_dirpath:
            dummy_deployments_dirpath = os.path.join(deployment_dirpath)

        small_dummy_deployment_source = AssetDeploymentSource(
            os.path.join(dummy_deployments_dirpath, 'small_dummy_deployment.zip'))
        large_dummy_deployment_source = AssetDeploymentSource(
            os.path.join(dummy_deployments_dirpath, 'large_dummy_deployment.zip'))

        S3LargeDeploymentResource(
            scope=self,
            name=f'{self.global_prefix()}SmallDummyDeployment',
            sources=[
                small_dummy_deployment_source
            ],
            destination_bucket=testing_destination_bucket,
            props=DeploymentProps(
                destination_key_prefix='small/',
                retain_on_delete=False
            )
        )

        S3LargeDeploymentResource(
            scope=self,
            name=f'{self.global_prefix()}LargeDummyDeployment',
            sources=[
                large_dummy_deployment_source
            ],
            destination_bucket=testing_destination_bucket,
            props=DeploymentProps(
                destination_key_prefix='large/',
                retain_on_delete=False,
                memory_limit=256,
                use_efs=True,
                vpc=testing_vpc,
                vpc_subnets=SubnetSelection(subnets=testing_vpc.private_subnets)
            )
        )
