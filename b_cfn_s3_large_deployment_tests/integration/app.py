from aws_cdk.core import App

from infrastructure import Infrastructure

# Initiate CDK applications and synthesize it.
app = App()
Infrastructure(app)
app.synth()
