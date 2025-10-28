import os
from azure.data.tables import TableServiceClient

def save_to_table_storage(student_id: str, student_name: str, score: float, workshop_id: str, comments: str, table_name: str="StudentGrades"):
    try:
        conn_str = os.getenv("AZURE_TABLES_CONNECTION_STRING")
        service = TableServiceClient.from_connection_string(conn_str=conn_str)
        table_client = service.get_table_client(table_name=table_name)
        entity = {
            "PartitionKey": str(student_id),
            "RowKey": str(workshop_id) if workshop_id else "default",
            "Score": score,
            "Name": student_name,
            "Comments": comments
        }   
        table_client.create_entity(entity=entity)
        print(f"Entity for student {student_name} saved successfully.")
    except Exception as e:
        print(f"Error saving entity for student {student_name}: {e}")