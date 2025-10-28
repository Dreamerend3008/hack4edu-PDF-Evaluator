import sys
import os
import azure.functions as func
import datetime
import json
import logging
import cgi
import io

# cosas a revisar
# fallo la subida a la tabla del blob storage por culpa de un valor null revisar eso



# use the src folder for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from saveTable import save_to_table_storage
from pdfEvaluation import evaluate_pdf
from utils.blob_client import get_blob_client

app = func.FunctionApp()

@app.route(route="uploadPDF", methods=["POST"])
def uploadPDF(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('PDF Upload triggered')
    try:
        content_type = req.headers.get('content-type', '')
        
        if 'multipart/form-data' in content_type:
            body = req.get_body()
            environ = {
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': content_type,
                'CONTENT_LENGTH': str(len(body))
            }
            
            form = cgi.FieldStorage(
                fp=io.BytesIO(body),
                environ=environ,
                keep_blank_values=True
            )
            
            container = 'pdf'
            blob_name = form.getvalue('blob_name')
            student_id = form.getvalue('student_id')
            student_name = form.getvalue('student_name')
            workshop_id = form.getvalue('workshop_id')

            file_field = form['file'] if 'file' in form else None
            file_bytes = file_field.file.read()
        else:
            return func.HttpResponse(json.dumps({"error": "multipart/form-data content-type required"}), status_code=400, mimetype="application/json")

        if not blob_name:
            return func.HttpResponse(json.dumps({"error": "blob_name is required"}), status_code=400, mimetype="application/json")

        blob_client = get_blob_client(container, blob_name)
        blob_client.upload_blob(file_bytes, overwrite=True)

        result = evaluate_pdf(container, blob_name, max_chars=50000, model="gpt-4o-mini")


        response_body = json.loads(result)
        table_name = "StudentGrades"
        score = response_body.get("score", 0.0) if isinstance(response_body, dict) else 0.0
        comments = response_body.get("comments", "") if isinstance(response_body, dict) else ""
        
        if student_id and student_name:
            try:
                save_to_table_storage(student_id, student_name, score, workshop_id, comments, table_name)
            except Exception:
                logging.exception("Failed to save to table storage")

        return func.HttpResponse(json.dumps(response_body), status_code=200, mimetype="application/json")
    
    except ValueError:
        return func.HttpResponse(json.dumps({"error": "bad request"}), status_code=400, mimetype="application/json")
    except Exception as e:
        logging.exception("Unhandled exception in uploadPDF")
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")

@app.route(route="uploadRubica", methods=["POST"])
def uploadRubrica(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Rubica Upload triggered')
    try:
        # Parse FormData from Alpine.js fetch with multipart/form-data
        content_type = req.headers.get('content-type', '')
        
        if 'multipart/form-data' in content_type:
            # Parse multipart form data using cgi module
            body = req.get_body()
            environ = {
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': content_type,
                'CONTENT_LENGTH': str(len(body))
            }
            
            form = cgi.FieldStorage(
                fp=io.BytesIO(body),
                environ=environ,
                keep_blank_values=True
            )
            
            # Extract form fields
            container = form.getvalue('container') or 'pdf'
            blob_name = form.getvalue('blob_name')
            
            # Get file from form
            file_field = form['file'] if 'file' in form else None
            if not file_field or not hasattr(file_field, 'file'):
                return func.HttpResponse(json.dumps({"error": "file is required"}), status_code=400, mimetype="application/json")
            
            file_bytes = file_field.file.read()
            filename = file_field.filename or blob_name
        else:
            return func.HttpResponse(json.dumps({"error": "multipart/form-data content-type required"}), status_code=400, mimetype="application/json")

        if not blob_name:
            return func.HttpResponse(json.dumps({"error": "blob_name is required"}), status_code=400, mimetype="application/json")

        # Upload file to blob storage
        blob_client = get_blob_client(container, blob_name)
        blob_client.upload_blob(file_bytes, overwrite=True)
        
        return func.HttpResponse(
            json.dumps({"message": f"File {filename} uploaded successfully to container {container}."}),
            status_code=200,
            mimetype="application/json"
        )
    except ValueError:
        return func.HttpResponse(json.dumps({"error": "bad request"}), status_code=400, mimetype="application/json")
    except Exception as e:
        logging.exception("Unhandled exception in uploadRubrica")
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")
# health check endpoint
@app.route(route="health", methods=["GET"])
def HealthCheck(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"status": "healthy", "version": "1.0"}),
        status_code=200,
        mimetype="application/json"
    )