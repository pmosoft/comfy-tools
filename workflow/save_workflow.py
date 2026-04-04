import json
import psycopg2
from psycopg2.extras import Json
from pathlib import Path

db = psycopg2.connect(host='onechart.iptime.org', dbname='media', user='media', password='m1234', port=5432);
cursor = db.cursor()

def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

WORKFLOW_DIR = Path(r"D:\pycharm-projects\ComfyUI\user\default\workflows")
json_files = list(WORKFLOW_DIR.glob("*.json"))
for path in json_files:
    name = path.stem
    description = f"{path.stem} workflow"
    workflow = load_json(path)

    sql = f""" delete from compy_workflow where name = '{name}' """;
    cursor.execute(sql)

    sql = """
    INSERT INTO compy_workflow (name, description, workflow)
    VALUES (%s, %s, %s)
    ON CONFLICT (name)
    DO UPDATE SET
        description = EXCLUDED.description,
        workflow = EXCLUDED.workflow,
        created_at = CURRENT_TIMESTAMP;
    """
    cursor.execute(sql,(name, description, Json(workflow)))

db.commit();
cursor.close();
