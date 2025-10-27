import sys
import os
import azure.functions as func
import datetime
import json
import logging

# use the src folder for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from pdfEvaluation import evaluate_pdf
from utils.blob_client import get_blob_client

app = func.FunctionApp()

@app.route(route="evaluatePDF", auth_level=func.AuthLevel.ANONYMOUS)
def evaluatePDF(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('PDF Eval triggered')
    try:
        # json procesing from the request
        req_body = req.get_json()
        container = req_body.get('container', 'pdf')
        blob_name = req_body.get('blob_name', 'texto.pdf')

        # logic from the python procesing
        result = evaluate_pdf(container, blob_name, max_chars=50000, model="gpt-4o-mini")
        return func.HttpResponse(result, status_code=200, mimetype="application/json")
    except ValueError:
        return func.HttpResponse("You made it trigger!! PDF EVAL", status_code=200)

@app.route(route="uploadPDF", methods=["POST"])
def uploadPDF(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('PDF Upload triggered')
    try:
        # form procesing from the request
        file = req.files.get("file")
        container = req.form.get('container')
        blob_name = req.form.get('blob_name')

        #blob storage upload logic
        blob_client = get_blob_client(container, blob_name)
        blob_client.upload_blob(file.stream, overwrite=True)
        
        return func.HttpResponse(
               f"File {file.filename} uploaded successfully to container {container}.",
               status_code=200
        )
    except ValueError:
        return func.HttpResponse("You made it trigger!! PDF UPLOAD", status_code=200)

# health check endpoint
@app.route(route="health", methods=["GET"])
def HealthCheck(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"status": "healthy", "version": "1.0"}),
        status_code=200,
        mimetype="application/json"
    )