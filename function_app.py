"""Azure Functions runtime entry point for BusinessInfinity workflows."""

import azure.functions as func
from business_infinity.workflows import aos_app

bp = aos_app.get_blueprint()
app = func.FunctionApp()
app.register_blueprint(bp)
