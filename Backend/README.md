## DOCUMENTACIÓN DE LAS FUNCIONES:
---> function_app.py
### uploadPDF

Descripción general:
Recibe una petición HTTPS que tiene un PDF para procesarlo.

Proceso:
* Recibe la petición y verifica que sea de tipo 'multipart/form-data' (es el que se recibe a la hora de crear un formulario)
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

### uploadRubrica
Descripción general: Recibe la información de los formularios para actualizar una rúbrica.

Proceso:
* Header de la rúbrica (valida al igual que la anterior función el tipo)
* Se comunica con el blob client y sube los cambios a la rúbrica
#### Excepciones
*    Bad request
*    Excepciones generales

