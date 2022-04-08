import logging

from b_aws_cf.stack import Stack
from b_aws_cf.stack_status import StackStatus

from b_cfn_s3_large_deployment_tests.integration.infrastructure import Infrastructure

logger = logging.getLogger(__name__)


def test_stack_created() -> None:
    """
    Tests that stack actually was created.
    :return: No return.
    """

    stack_name = Infrastructure.name()
    stack = Stack.from_name(stack_name)
    assert stack.stack_status in [
        StackStatus.CREATE_COMPLETE,
        StackStatus.UPDATE_COMPLETE
    ]
