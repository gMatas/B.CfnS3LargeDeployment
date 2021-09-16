import logging

from b_aws_testing_framework.credentials import Credentials

from b_cfn_s3_large_deployment_tests.integration.infrastructure import Infrastructure

logger = logging.getLogger(__name__)


def test_stack_created() -> None:
    """
    Tests that stack actually was created.
    :return: No return.
    """

    client = Credentials().boto_session.client('cloudformation')

    stacks = client.list_stacks(StackStatusFilter=['CREATE_COMPLETE'])['StackSummaries']
    stacks = [stack['StackName'] for stack in stacks]

    assert Infrastructure.name() in stacks
