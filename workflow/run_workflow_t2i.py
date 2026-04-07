import json
import requests

COMFY_URL = "http://pmosoft.iptime.org:8188/prompt"


def load_workflow(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def set_prompt(workflow, new_prompt):
    #for node_id, node in workflow["nodes"].items():
    for node_id, node in workflow.items():
        if node.get("class_type") == "CLIPTextEncode":
            node["inputs"]["text"] = new_prompt
    return workflow

def run_workflow(workflow):
    payload = {
        "prompt": workflow
    }
    res = requests.post(COMFY_URL, json=payload)
    return res.json()

# 실행
workflow = load_workflow(r"d:\pycharm-projects\ComfyUI\user\default\workflows\t2i_api.json")


# 🔥 프롬프트 변경
workflow = set_prompt(workflow, "a beautiful japenese model, studio lighting, ultra realistic")

# 실행
result = run_workflow(workflow)

print(result)