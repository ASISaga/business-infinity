"""Azure Functions runtime entry point for BusinessInfinity workflows."""

from business_infinity.workflows import app as workflows_app

app = workflows_app.get_functions()
functions = app
