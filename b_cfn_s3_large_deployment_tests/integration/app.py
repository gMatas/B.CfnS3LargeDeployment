from aws_cdk.core import App

from b_cfn_s3_large_deployment_tests.integration.infrastructure import Infrastructure

# Initiate CDK applications and synthesize it.
app = App()
Infrastructure(app)
app.synth()
