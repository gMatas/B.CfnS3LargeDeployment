import logging

from aws_cdk.core import App
from b_aws_testing_framework.tools.cdk_testing.testing_manager import TestingManager

from infrastructure import Infrastructure

logger = logging.getLogger(__name__)


try:
    TestingManager.set_global_prefix()

    # Initiate CDK applications and synthesize it.
    app = App()
    Infrastructure(app)
    app.synth()
except Exception as e:
    logger.error(f'Exception raised {repr(e)}')
finally:
    TestingManager.delete_global_prefix()
