"""Azure Functions runtime entry point for BusinessInfinity workflows."""

from business_infinity.workflows import app

functions = app.get_functions()
app = functions
