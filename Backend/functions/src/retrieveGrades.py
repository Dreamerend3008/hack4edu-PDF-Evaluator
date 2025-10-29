import os
from azure.data.tables import TableServiceClient

conn_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
table_name = "StudentGrades"

table_client = TableServiceClient.from_connection_string(conn_string).get_table_client(table_name)

def get_student_grades(student_id: str) -> list:
    query_filter = f"PartitionKey eq '{student_id}'"
    grades = list(table_client.query_entities(query_filter))
    return grades

def calculate_average(grades):
    if not grades:
        return 0
    total = sum(float(grade['Score']) for grade in grades)
    return total / len(grades)

def build_grade_report(student_grades):
    if not student_grades:
        return None
    
    student_id = student_grades[0]['PartitionKey']
    grades = []

    for grade in student_grades:
        grades.append({'Score': grade.get('Score', 0), 'workshop_id': grade.get('RowKey', '')})
    
    average = calculate_average(grades)

    student_json = {
        "student_id": student_id,
        "student_name": student_grades[0].get('Name', ''),
        "grades": grades,
        "average_grade": average
    }
    return student_json
def get_all_student_ids():
    all_entities = list(table_client.query_entities(""))
    student_ids = set(entity['PartitionKey'] for entity in all_entities)
    return list(student_ids)

def retrieve_grades()->str:
    # Implementation for retrieving grades
    student_ids = get_all_student_ids()
    all_students_report = []

    for student_id in student_ids:
        student_grades = get_student_grades(student_id)
        student_report = build_grade_report(student_grades)
        if student_report:
            all_students_report.append(student_report)

    return all_students_report