import json
import psycopg2
import requests
import uuid


def get_workflow_from_db(name: str) -> dict:
    db = psycopg2.connect(host='onechart.iptime.org', dbname='media', user='media', password='m1234', port=5432);
    cursor = db.cursor()
    sql = f""" select workflow from compy_workflow where name = '{name}' """;
    cursor.execute(sql)
    row = cursor.fetchone()
    db.commit();cursor.close()

    return row[0]

if __name__ == "__main__":
    client_id = str(uuid.uuid4())

    name = 't2i_api'
    workflow = get_workflow_from_db(name)

    response = requests.post(
        f"http://pmosoft.iptime.org:8188/prompt",
        json={"prompt": workflow, "client_id": client_id}
    )

    response.raise_for_status()
    result = response.json()

