import json 
import azure.functions as func

from utils.load_bytes import load_bytes
from utils.pdf_bytes_to_text import pdf_bytes_to_text
from utils.get_oai_client import get_oai_client
from utils.get_rubrica import get_rubrica
from openai import AzureOpenAI


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

def evaluate_pdf(container: str, blob_name:str, workshop_id: str, max_chars:int, model:str):
    try:
        rubrica_prompt = """Eres un evaluador. Recibirás un TEXTO y debes calificarlo según esta rúbrica:"""
        formato_json = """"Devuelve exclusivamente un JSON con el siguiente formato. Siempre incluye exactamente 5 criterios y califica de 0 a 5, manten los comentarios cortos:
{
  "score": float,
  "comments": string,
  "criteria": [
    {
      "name": "Claridad",
      "rating": string,
      "feedback": string
    },
    {
      "name": "Relevancia",
      "rating": string,
      "feedback": string
    },
    {
      "name": "Tono",
      "rating": string,
      "feedback": string
    },
    {
      "name": "Justificación",
      "rating": string,
      "feedback": string
    },
    {
      "name": "Observaciones generales",
      "rating": string,
      "feedback": string
    }
  ],
  "summary": string
} """

        pdf_bytes = load_bytes(container, blob_name)
        text = pdf_bytes_to_text(pdf_bytes, max_chars=max_chars)

        client = get_oai_client()

        # select the rubrica made for the evaluation
        rubrica_prompt += get_rubrica(workshop_id) + formato_json

        messages = [
            {"role": "system", "content": rubrica_prompt},
            {"role": "user", "content": f"Evalua este texto usando la rubrica:{text}"}
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.0,
            response_format={"type": "json_object"},
            max_tokens=5000
        )
        result = response.choices[0].message.content
        return result

    except Exception as e:
        return {"error": str(e)}    
