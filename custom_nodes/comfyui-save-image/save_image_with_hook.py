import os
import numpy as np
from PIL import Image
from nodes import SaveImage  # 기본 SaveImage 노드 임포트

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
        # **kwargs를 추가하여 ComfyUI가 자동으로 보내는 prompt, extra_pnginfo 등을 모두 받아냅니다.
        
        # 1. 기존 저장 로직 실행 (부모 클래스인 SaveImage의 save_images 호출)
        # 부모 클래스에게도 받은 인자들을 그대로 전달해줍니다.
        results = super().save_images(images, filename_prefix, **kwargs)
        
        # 2. Python Hook 실행 (저장 후 작업)
        if "ui" in results and "images" in results["ui"]:
            for result in results["ui"]["images"]:
                # 결과에서 파일명 추출
                filename = result["filename"]
                subfolder = result.get("subfolder", "")
                
                # 전체 경로 생성
                full_path = os.path.join(self.output_dir, subfolder, filename)
                
                # 훅 실행
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

        except Exception as e:
            print(f"❌ 이동 실패: {e}")
        
NODE_CLASS_MAPPINGS = {
    "SaveImageWithHook": SaveImageWithHook
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImageWithHook": "💾 Save Image with Python Hook"
}        