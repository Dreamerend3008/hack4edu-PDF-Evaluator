import sys
import os
import azure.functions as func
import datetime
import json
import logging
import cgi
import io


# use the src folder for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from saveTable import save_to_table_storage
from pdfEvaluation import evaluate_pdf
from utils.blob_client import get_blob_client

app = func.FunctionApp()

@app.route(route="uploadPDF", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
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

        result = evaluate_pdf(container, blob_name, workshop_id,max_chars=50000, model="gpt-4o-mini")


        # some error in the json managment
        if isinstance(result, (str, bytes, bytearray)):
            try:
                response_body = json.loads(result)
            except Exception:
                logging.warning("evaluate_pdf returned non-JSON string")
                response_body = {"raw": result}
        elif isinstance(result, dict):
            response_body = result
        else:
            response_body = {"raw": str(result)}

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

@app.route(route="uploadRubica", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def uploadRubrica(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Rubica Upload triggered')
    try:
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
            
            container = 'rubicas'
            blob_name = form.getvalue('workshop_id')
            blob_name = blob_name + '.txt'

            text = str(form.getvalue('text'))
        else:
            return func.HttpResponse(json.dumps({"error": "multipart/form-data content-type required"}), status_code=400, mimetype="application/json")

        if not blob_name:
            return func.HttpResponse(json.dumps({"error": "blob_name is required"}), status_code=400, mimetype="application/json")

        # Upload file to blob storage
        blob_client = get_blob_client(container, blob_name)
        blob_client.upload_blob(text, overwrite=True)

        return func.HttpResponse(
            json.dumps({"message": f"File {blob_name} uploaded successfully to container {container}."}),
            status_code=200,
            mimetype="application/json"
        )
    except ValueError:
        return func.HttpResponse(json.dumps({"error": "bad request"}), status_code=400, mimetype="application/json")
    except Exception as e:
        logging.exception("Unhandled exception in uploadRubrica")
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")
# health check endpoint
@app.route(route="health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def HealthCheck(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"status": "healthy", "version": "1.0"}),
        status_code=200,
        mimetype="application/json"
    )