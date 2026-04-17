"""Azure Functions runtime entry point for BusinessInfinity workflows."""

from business_infinity.workflows import app as workflow_app

app = workflow_app.get_functions()
