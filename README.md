# PDFSSOR

## Resumen

 PDFSSOR es una plataforma web desarrollada por estudiantes de la Pontificia Universidad Javeriana para facilitar y acelerar la evaluación mediante rúbricas digitales. El sistema integra funcionalidades de IA (Azure AI Foundry) para generar sugerencias de retroalimentación y automatizar tareas repetitivas, mejorando la transparencia en la entrega de notas y reduciendo el tiempo que los docentes dedican a la corrección.

Problema detectado:
- Los profesores invierten demasiado tiempo en revisar rúbricas y escribir retroalimentación para cada estudiante.
- Muchos de los trabajos calificados en especial en el formato de texto son expuestos a criterios poco objetivos e incluso sesgados durante su evaluación.
- Los estudiantes no siempre comprenden los criterios ni la retroalimentación.


Qué ofrece la solución:
- Interfaz para calificar rúbricas.
- Retroalimentación automática usando IA.
- Historial y gestión de calificaciones.
- Integración con servicios de almacenamiento (blob) y funciones serverless para procesar PDFs y extraer información.

Este proyecto tuvo como resultado el deploy de una pagina web en github-pages que interactua con el backend a través de azure functions.

[Link de la pagina web](https://dreamerend3008.github.io/hack4edu-PDF-Evaluator/)

## Estructura del repositorio (resumen)

Raíz del proyecto:

- `Backend/` : código de backend (Azure Functions en Python).
  - `functions/` : definiciones de las funciones desplegables.
  - `function_app.py` : punto central que registra/agrupa las funciones (Azure Functions app).
  - `host.json` : configuración de runtime de Azure Functions.
  - `requirements.txt` : dependencias Python del backend.
  - `src/` : lógica de negocio y módulos reutilizables.
    - `pdfEvaluation.py`, `retrieveGrades.py`, `saveTable.py` : manejan la evaluación de PDFs, recuperación de notas y persistencia.
    - `utils/` : utilidades auxiliares como `blob_client.py`, `get_oai_client.py`, etc.

- `Frontend/` y `docs/` : código y recursos del frontend y documentación estática.

## Arquitectura del backend (detallada)

El backend está diseñado como un conjunto de funciones serverless (Azure Functions) escritas en Python. A continuación se explica su funcionamiento:

- Azure Functions (carpeta `functions/` y `function_app.py`):
  - Cada endpoint o tarea pesada está implementada como una función independiente por ejemplo, endpoints HTTP que reciben un PDF, desencadenan su procesamiento y devuelven resultados JSON.
  - `function_app.py` actúa como el punto de registro de funciones de la aplicación (punto de entrada para Azure Functions en este proyecto).

- Configuración y dependencias:
  - `host.json` contiene ajustes del runtime (timeouts, logging, extensiones).
  - `requirements.txt` lista paquetes necesarios (requests, azure-storage-blob, azure-functions, openai/azure-openai client, pdf processing libs, etc.).
  - `local.settings.json` no se incluye en el repositorio pero es necesaria para la ejecución local debido a que contiene las variables de entorno como: **AZURE_OPENAI_KEY**

- Flujo principal de procesamiento (resumen):
  1. El frontend sube un PDF o el docente lo envía vía un formulario. El request llega a una Function HTTP.
 2. La Function usa utilidades en `src/` para leer los bytes (`load_bytes.py`) y convertir el PDF a texto (`pdf_bytes_to_text.py`).
 3. El texto y/o los metadatos se envían al cliente de IA (implementado en `get_oai_client.py`) para extraer la rúbrica, sugerencias y/o notas (vía `get_rubrica.py` o `pdfEvaluation.py`).
 4. Resultados estructurados (rúbrica, puntuaciones, comentarios recomendados) se guardan en Blob Storage o en una tabla mediante `saveTable.py` y/o `blob_client.py`.
 5. Para consultas posteriores, `retrieveGrades.py` expone endpoints que recuperan y devuelven las calificaciones almacenadas.

- Integraciones clave:
  - Azure Blob Storage: para almacenar PDFs, outputs y datos persistentes. Interacción a través de `blob_client.py`.
  - Azure/OpenAI (o cliente OpenAI): para generar sugerencias de retroalimentación y extraer estructura de la rúbrica (archivo `get_oai_client.py`).

- Consideraciones de seguridad y configuración:
  - No guardar claves en `local.settings.json` dentro del repositorio público.
  - Usar variables de entorno en el entorno de ejecución (Azure Functions) o Azure Key Vault para secretos.
  - Limitar el tamaño máximo de archivos y validar el contenido entrante antes de procesar.

## Cómo ejecutar el backend localmente (resumen)

Requisitos mínimos:
- Python 3.8+ (ver `requirements.txt`).
- Azure Functions Core Tools (para ejecutar funciones localmente). Opcionalmente Docker.
- Cuenta de azure con creditos para crear AI foundry agents, Functionapps, Blob storage

Pasos básicos:
1. Posicionarse en la carpeta `Backend`.
2. Activar entorno de python
3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar variables locales: copiar `local.settings.json` y configurar las claves necesarias (`AzureWebJobsStorage`, `OPENAI_API_KEY` o `AZURE_OPENAI_*`, etc.).

4. Iniciar las Azure Functions localmente (si tiene las herramientas instaladas):

```bash
func start
```

5. Probar los endpoints HTTP desde el frontend o con curl/Postman.


## Mejoras futuras

Buscando el uso de este proyecto como una herramienta a futuro muy util para profesores y estudiantes nuestra propuesta a futuro de nuestro proyecto se encuentra en `FutureFeatures.md`

---
