import os
import sys

from aws_cdk.core import App

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_PATH)

from b_cfn_s3_large_deployment_tests.testing_infrastructure import TestingInfrastructure

app = App()
TestingInfrastructure(app)
app.synth()
