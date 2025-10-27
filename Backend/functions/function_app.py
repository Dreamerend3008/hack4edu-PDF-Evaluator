import sys
import os
import azure.functions as func
import datetime
import json
import logging

# use the src folder for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from pdfEvaluation import evaluate_pdf

app = func.FunctionApp()

@app.route(route="evaluatePDF", auth_level=func.AuthLevel.ANONYMOUS)
def evaluatePDF(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('PDF Eval triggered')

    name = req.params.get('name')
    if not name:
        try:
            # json procesing from the request
            req_body = req.get_json()
            container = req_body.get('container', 'pdf')
            blob_name = req_body.get('blob_name', 'texto.pdf')

            # logic from the python procesing
            result = evaluate_pdf(container, blob_name, max_chars=50000, model="gpt-4o-mini")
            return func.HttpResponse(result, status_code=200, mimetype="application/json")
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )