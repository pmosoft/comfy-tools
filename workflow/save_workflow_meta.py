import json


def extract_ltx23_metadata(workflow_path):
    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    metadata = {
        "positive_prompt": "",
        "negative_prompt": "",
        "seed_stage1": None,
        "seed_stage2": None,
        "cfg_stage1": None,
        "cfg_stage2": None,
        "width": None,
        "height": None,
        "length": None,
        "fps_render": None,
        "fps_output": None,
        "checkpoint": "",
        "lora": "",
        "upscaler": "",
        "model_name": "LTX 2.3"
    }

    nodes = workflow.get("nodes", [])

    for node in nodes:
        node_type = node.get("type", "")
        values = node.get("widgets_values", [])

        # Positive Prompt
        if node_type == "CLIPTextEncode" and len(values) > 0:
            text = values[0]
            if text and len(text) > len(metadata["positive_prompt"]):
                metadata["positive_prompt"] = text

        # Negative Prompt (빈 문자열일 수 있음)
        if node_type == "CLIPTextEncode" and len(values) > 0:
            text = values[0]
            if text == "":
                metadata["negative_prompt"] = text

        # Random seeds
        if node_type == "RandomNoise":
            seed = values[0]
            if metadata["seed_stage1"] is None:
                metadata["seed_stage1"] = seed
            else:
                metadata["seed_stage2"] = seed

        # CFG values
        if node_type == "CFGGuider":
            cfg = values[0]
            if metadata["cfg_stage1"] is None:
                metadata["cfg_stage1"] = cfg
            else:
                metadata["cfg_stage2"] = cfg

        # Video latent settings
        if node_type == "EmptyImage":
            metadata["width"] = values[0]
            metadata["height"] = values[1]
            metadata["length"] = values[2]

        # Render FPS
        if node.get("title") == "Frame Rate(float)":
            metadata["fps_render"] = values[0]

        # Output video FPS
        if node_type == "VHS_VideoCombine":
            if isinstance(values, dict):
                metadata["fps_output"] = values.get("frame_rate")

        # Checkpoint
        if node_type == "CheckpointLoaderSimple":
            metadata["checkpoint"] = values[0]

        # LoRA
        if node_type == "LoraLoaderModelOnly":
            metadata["lora"] = values[0]

        # Upscaler
        if node_type == "LatentUpscaleModelLoader":
            metadata["upscaler"] = values[0]

    return metadata


if __name__ == "__main__":
    workflow_path = r"d:\pycharm-projects\ComfyUI\user\default\workflows\t2v_ltx2.3_shorts_01.json"

    meta = extract_ltx23_metadata(workflow_path)

    print(json.dumps(meta, indent=4, ensure_ascii=False))