import os

from b_aws_testing_framework.credentials import Credentials
from b_aws_testing_framework.tools.cdk_testing.cdk_tool_config import CdkToolConfig
from b_aws_testing_framework.tools.cdk_testing.testing_manager import TestingManager

CDK_PATH = os.path.dirname(os.path.abspath(__file__))

manager = TestingManager(Credentials(), CdkToolConfig(CDK_PATH))


def pytest_configure(*args, **kwargs):
    """
    Called after command line options have been parsed and
    all plugins and initial conftest files been loaded.
    """

    manager.set_global_prefix()
    manager.prepare_infrastructure()


def pytest_unconfigure(*args, **kwargs):
    """
    Called before test process is exited.
    """

    manager.destroy_infrastructure()
