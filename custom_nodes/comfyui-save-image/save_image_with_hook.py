import os
import requests

from nodes import SaveImage  # 기본 SaveImage 노드 임포트

COMFY_URL = "http://pmosoft.iptime.org:8188"

class SaveImageWithHook(SaveImage):
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(s):
        # 기존 SaveImage의 입력값에 'hook_script' 등을 추가할 수 있습니다.
        inputs = SaveImage.INPUT_TYPES()
        inputs["required"]["payload_info"] = ("STRING", {"default": "none"})
        return inputs

    def save_images(self, images, filename_prefix="ComfyUI", payload_info="none", **kwargs):

        # 🔥 kwargs에서 실제 filename_prefix 가져오기
        real_prefix = kwargs.get("filename_prefix", filename_prefix)

        results = super().save_images(images, real_prefix, **kwargs)

        if "ui" in results and "images" in results["ui"]:
            for result in results["ui"]["images"]:
                filename = result["filename"]
                subfolder = result.get("subfolder", "")

                full_path = os.path.join(self.output_dir, subfolder, filename)

                self.execute_python_hook(full_path, payload_info)

        return results

    def execute_python_hook(self, image_path, info):
        import os
        import shutil

        print(f"--- [Hook Executed] ---")
        print(f"Saved Image Path: {image_path}")
        print(f"Additional Info: {info}")

        try:
            # 🔥 원본 경로
            full_path = image_path

            # 🔥 temp 경로 생성
            rel_path = os.path.relpath(full_path, self.output_dir)
            temp_path = os.path.join(self.output_dir, "temp", rel_path)

            # 🔥 temp 폴더 생성 (없으면)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)

            # 🔥 파일 이동
            shutil.move(full_path, temp_path)

            print(f"📁 이동 완료 → {temp_path}")

            # 🔥 history 삭제
            res = requests.post(f"{COMFY_URL}/history/clear")
            print(f"🧹 history 삭제: {res.json()}")

        except Exception as e:
            print(f"❌ 이동 실패: {e}")
        
NODE_CLASS_MAPPINGS = {
    "SaveImageWithHook": SaveImageWithHook
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImageWithHook": "💾 Save Image with Python Hook"
}        