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
        # 여기에 실행하고 싶은 파이썬 코드를 작성합니다.
        print(f"--- [Hook Executed] ---")
        print(f"Saved Image Path: {image_path}")
        print(f"Additional Info: {info}")
        # 예: 외부 DB 저장, Discord 알림 발송, AI 분석 모델 연동 등
        
NODE_CLASS_MAPPINGS = {
    "SaveImageWithHook": SaveImageWithHook
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImageWithHook": "💾 Save Image with Python Hook"
}        