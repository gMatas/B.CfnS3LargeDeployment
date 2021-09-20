from b_cfn_s3_large_deployment_tests.integration.manager import GLOBAL_MANAGER


def pytest_configure(*args, **kwargs):
    """
    Called after command line options have been parsed and
    all plugins and initial conftest files been loaded.
    """

    GLOBAL_MANAGER.prepare_infrastructure()


def pytest_unconfigure(*args, **kwargs):
    """
    Called before test process is exited.
    """

    GLOBAL_MANAGER.destroy_infrastructure()
