## DOCUMENTACIÓN DE LAS FUNCIONES:
---> function_app.py
### uploadPDF

Descripción general:
* Recibe una petición HTTPS que tiene un archivo PDF (verifica que sea de tipo 'multipart/form-data', que es el que se recibe a la hora de crear un formulario)
* Extrae información importante del archivo como:
*   Nombre del estudiante
*   Header del pdf
*   Número del taller
*   El archivo en sí
* Sube el PDF al blob storage
* Evalua el PDF usando IA
* Interpreta el resultado de la IA
* Almacena la calificación y los resultados en la Aure Table Storage
* Retorna un JSON con los resultados

#### Excepciones
Leer el head
*    Bad request
*    Excepciones generales
Cargar el JSON
*    warning: "evaluate_pdf returned non-JSON string"
