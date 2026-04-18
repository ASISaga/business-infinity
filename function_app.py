import azure.functions as func
from business_infinity.additional_blueprints import boardroom_blueprint, seo_blueprint
from business_infinity.workflows import aos_app

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Register the AOS Blueprint
bp = aos_app.get_blueprint()
app.register_blueprint(bp)
app.register_blueprint(boardroom_blueprint)
app.register_blueprint(seo_blueprint)

# Add this to force the host to acknowledge the app instance
@app.route(route="ping", methods=["GET"])
def ping(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("BusinessInfinity Host Active", status_code=200)
