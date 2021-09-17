import os

from b_aws_testing_framework.credentials import Credentials
from b_aws_testing_framework.tools.cdk_testing.cdk_tool_config import CdkToolConfig
from b_aws_testing_framework.tools.cdk_testing.testing_manager import TestingManager

GLOBAL_PREFIX = os.getenv('GLOBAL_PREFIX')
CDK_PATH = f'{os.path.dirname(os.path.abspath(__file__))}'
GLOBAL_MANAGER = TestingManager(Credentials(), CdkToolConfig(CDK_PATH))

if GLOBAL_PREFIX:
    GLOBAL_MANAGER.set_global_prefix(f'B{GLOBAL_PREFIX[:10]}')
