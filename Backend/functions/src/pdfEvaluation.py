import json 
import azure.functions as func

from utils.load_pdf_bytes import load_pdf_bytes
from utils.pdf_bytes_to_text import pdf_bytes_to_text
from utils.get_oai_client import get_oai_client
from openai import AzureOpenAI

RUBICA_PROMPT = """Eres un evaluador. Recibirás un TEXTO y debes calificarlo según esta rúbrica:

- Claridad (0–5): ¿El texto es comprensible, directo y bien estructurado?
- Relevancia (0–5): ¿Responde al objetivo/tema sin divagar?
- Tono (0–5): ¿Mantiene un tono adecuado para un entorno profesional?

Calcula una puntuación TOTAL (0–100) ponderando así:
- Claridad 40%
- Relevancia 40%
- Tono 20%

Devuelve exclusivamente un JSON que cumpla el esquema proporcionado.
No incluyas texto adicional fuera del JSON.

Si algo no se puede evaluar, asigna 0 y explica brevemente en "justificacion".
"""


def main(req: func.HttpRequest) -> func.HttpRequest:
    try:
        if req.method == "POST":
            data = req.get_json(silent=True) or {}
        else: 
            data = req.params or {}
        
        container = data.get("container")
        blob_name = data.get("blob_name")
        model = "gpt-4o-mini"
        max_chars = 50000
        result = evaluate_pdf(container, blob_name, max_chars, model)
        return func.HttpResponse(json.dumps(result), status_code=200, mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")

def evaluate_pdf(container: str, blob_name:str, max_chars:int, model:str):
    try:
        pdf_bytes = load_pdf_bytes(container, blob_name)
        text = pdf_bytes_to_text(pdf_bytes, max_chars=max_chars)

        client = get_oai_client()

        messages = [
            {"role": "system", "content": RUBICA_PROMPT},
            {"role": "user", "content": f"Evalua este texto usando la rubica:{text}"}
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.0,
            response_format={"type": "json_object"},
            max_tokens=5000
        )
        return response.choices[0].message.content
    except Exception as e:
        return {"error": str(e)}    
