import os
from dataclasses import dataclass

from aws_cdk.aws_ec2 import SubnetConfiguration, SubnetType, Vpc, SubnetSelection
from aws_cdk.aws_s3 import Bucket
from aws_cdk.core import Construct, RemovalPolicy
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack

from b_cfn_s3_large_deployment.deployment_props import DeploymentProps
from b_cfn_s3_large_deployment.deployment_source import AssetDeploymentSource
from b_cfn_s3_large_deployment.resource import S3LargeDeploymentResource
from b_cfn_s3_large_deployment_tests.integration import ROOT_PATH


class Infrastructure(TestingStack):
    @dataclass(frozen=True)
    class __DeploymentOutputKeys:
        source_name: str
        destination_bucket_name: str
        destination_bucket_key_prefix: str

    SMALL_DEPLOYMENT_OUTPUT_KEYS = __DeploymentOutputKeys(
        source_name='small_dummy_deployment',
        destination_bucket_name='SmallDeploymentDestinationBucketName',
        destination_bucket_key_prefix='SmallDeploymentDestinationBucketPrefixKey',
    )
    LARGE_DEPLOYMENT_OUTPUT_KEYS = __DeploymentOutputKeys(
        source_name='large_dummy_deployment',
        destination_bucket_name='LargeDeploymentDestinationBucketName',
        destination_bucket_key_prefix='LargeDeploymentDestinationBucketPrefixKey',
    )
    LARGE_EFS_DEPLOYMENT_OUTPUT_KEYS = __DeploymentOutputKeys(
        source_name='large_dummy_deployment',
        destination_bucket_name='LargeEfsDeploymentDestinationBucketName',
        destination_bucket_key_prefix='LargeEfsDeploymentDestinationBucketPrefixKey',
    )

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

        dummy_deployments_dirpath = os.path.join(ROOT_PATH, 'dummy_deployments')

        small_dummy_deployment_source = AssetDeploymentSource(
            os.path.join(dummy_deployments_dirpath, self.SMALL_DEPLOYMENT_OUTPUT_KEYS.source_name))
        large_dummy_deployment_source = AssetDeploymentSource(
            os.path.join(dummy_deployments_dirpath, self.LARGE_DEPLOYMENT_OUTPUT_KEYS.source_name))
        large_dummy_efs_deployment_source = AssetDeploymentSource(
            os.path.join(dummy_deployments_dirpath, self.LARGE_EFS_DEPLOYMENT_OUTPUT_KEYS.source_name))

        small_deployment = S3LargeDeploymentResource(
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
        large_deployment = S3LargeDeploymentResource(
            scope=self,
            name=f'{self.global_prefix()}LargeDummyDeployment',
            sources=[large_dummy_deployment_source] * 2,
            destination_bucket=testing_destination_bucket,
            props=DeploymentProps(
                destination_key_prefix='large/',
                retain_on_delete=False,
                memory_limit=1024,
                ephemeral_storage_size=1024
            )
        )
        large_efs_deployment = S3LargeDeploymentResource(
            scope=self,
            name=f'{self.global_prefix()}LargeEfsDummyDeployment',
            sources=[large_dummy_efs_deployment_source],
            destination_bucket=testing_destination_bucket,
            props=DeploymentProps(
                destination_key_prefix='large-efs/',
                retain_on_delete=False,
                memory_limit=1024,
                use_efs=True,
                vpc=testing_vpc,
                vpc_subnets=SubnetSelection(subnets=testing_vpc.private_subnets)
            )
        )

        self.__add_deployment_outputs(self.SMALL_DEPLOYMENT_OUTPUT_KEYS, small_deployment)
        self.__add_deployment_outputs(self.LARGE_DEPLOYMENT_OUTPUT_KEYS, large_deployment)
        self.__add_deployment_outputs(self.LARGE_EFS_DEPLOYMENT_OUTPUT_KEYS, large_efs_deployment)

    def __add_deployment_outputs(
            self,
            deployment_output_keys: __DeploymentOutputKeys,
            deployment: S3LargeDeploymentResource,
    ) -> None:
        self.add_output(deployment_output_keys.destination_bucket_name, deployment.destination_bucket_name)
        self.add_output(deployment_output_keys.destination_bucket_key_prefix, deployment.destination_bucket_key_prefix)
