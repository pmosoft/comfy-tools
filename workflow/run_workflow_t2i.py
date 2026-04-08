import json
import requests
import time
import re

COMFY_URL = "http://pmosoft.iptime.org:8188"

# -----------------------
# workflow 로드
# -----------------------
def load_workflow(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------
# workflow 수정
# -----------------------

def make_filename(prompt, steps, sampler, scheduler, shift):
    # 1. 프롬프트 첫 구문 추출 (콤마 기준)
    first_part = prompt.split(",")[0]

    # 2. 공백 → _
    first_part = first_part.strip().replace(" ", "_")

    # 3. 특수문자 제거 (파일명 안전)
    first_part = re.sub(r'[^a-zA-Z0-9_가-힣]', '', first_part)

    # 4. 길이 제한 (선택)
    first_part = first_part[:20]

    return f"{first_part}_{steps}_{sampler}_{scheduler}_{shift}"


def update_workflow(workflow, prompt, width, height, control_mode, steps, sampler_name, scheduler, shift):
    filename = make_filename(prompt, steps, sampler_name, scheduler, shift)

    for node_id, node in workflow.items():
        # prompt
        if node.get("class_type") == "CLIPTextEncode":
            node["inputs"]["text"] = prompt

        # EmptySD3LatentImage
        if node.get("class_type") == "EmptySD3LatentImage":
            node["inputs"]["width"] = width
            node["inputs"]["height"] = height

        # KSampler
        if node.get("class_type") == "KSampler":
            node["inputs"]["control_after_generate"] = control_mode
            node["inputs"]["steps"] = steps
            node["inputs"]["sampler_name"] = sampler_name
            node["inputs"]["scheduler"] = scheduler

        if node.get("class_type") == "ModelSamplingAuraFlow":
            node["inputs"]["shift"] = shift

        # 🔥 SaveImage 파일명 변경
        if node.get("class_type") == "SaveImage":
            node["inputs"]["filename_prefix"] = filename

    return workflow


def queue_prompt(workflow):
    res = requests.post(f"{COMFY_URL}/prompt", json={"prompt": workflow})
    return res.json()["prompt_id"]

# ============================
# 🔥 배치 설정
# ============================

prompt_list = [
    "beautiful woman golfer, realistic, 4k",
]

# prompt_list = [
#     "Extreme close-up rear view of anal sex in doggy style, beautiful woman on all fours on bed, back deeply arched, hips raised high, ass cheeks spread wide by the man's strong hands gripping both buttocks firmly. His thick erect penis halfway inserted into her tight anus, clear stretching and penetration visible from behind, glistening lube dripping down, realistic anus and cock details, sweat on skin, raw and intense erotic atmosphere, photorealistic, ultra detailed, sharp focus on penetration, cinematic lighting, 8k --ar 16:9",
#     "Low angle rear close-up of intense doggy style anal intercourse. Gorgeous woman kneeling on bed with hips pushed high, back arched dramatically, round ass presented. Muscular man behind her, both hands spreading her ass cheeks apart, his thick cock penetrating halfway into her anus, detailed view of stretched anus and half-inserted penis from below, shiny fluids, realistic anatomy, dramatic side lighting, highly explicit, photorealistic, 8k",
#     "Close-up side-front view of anal doggy style sex. Beautiful woman on all fours, head turned sideways with pleasure expression, mouth slightly open, back arched, hips high. Man kneeling behind gripping her ass cheeks tightly with both hands, his penis halfway buried in her anus, visible penetration from the side, detailed realistic anatomy, sweat glistening on bodies, warm bedroom lighting, sensual yet explicit, ultra photorealistic, high resolution",
#     "First person over-the-shoulder POV close-up of anal sex in classic doggy style. Man’s hands firmly gripping the woman’s round ass cheeks spreading them, his thick cock halfway inside her tight anus, deep arched back, hips raised, detailed penetration and stretching visible, glistening lube, realistic skin texture, intimate and immersive view, photorealistic, highly detailed, erotic atmosphere",
#     "High angle close-up view from above of doggy style anal penetration. Attractive woman on hands and knees on bed, back curved deeply, ass up. Man behind her holding both ass cheeks firmly with his hands, thick penis inserted halfway into her anus, clear top-down view of penetration, realistic details, soft overhead lighting casting gentle shadows, ultra detailed, cinematic, 8k",
#     "Extreme macro close-up of anal penetration in doggy style. Woman’s ass cheeks spread wide by strong male hands, thick veiny cock halfway inserted into her tight glistening anus, detailed stretching, shiny lube and slight gape, realistic skin pores and textures, sharp focus, explicit medical-level detail, photorealistic, high resolution",
# ]

width = 480; height = 640

control_mode = "fixed"
#control_mode = "randomize"

steps_list = [10]

sampler_scheduler_shift_list = [
    ("dpmpp_2m", "karras", 2),
    ("dpmpp_2m_sde", "karras", 2),
    ("dpmpp_sde", "karras", 5),
    ("uni_pc", "normal", 3),
    ("euler", "normal", 2),
]

workflow_path = r"d:\pycharm-projects\ComfyUI\user\default\workflows\t2i\t2i_api.json"

# ============================
# 🚀 실행
# ============================

base_workflow = load_workflow(workflow_path)

count = 0

for prompt in prompt_list:
    for steps in steps_list:
        for sampler, scheduler, shift in sampler_scheduler_shift_list:
            wf = json.loads(json.dumps(base_workflow))  # deepcopy

            wf = update_workflow(
                wf,
                prompt,
                width,
                height,
                control_mode,
                steps,
                sampler,
                scheduler,
                shift
            )

            result = queue_prompt(wf)

            count += 1
            print(f"[{count}] 완료 → prompt='{prompt[:20]}...' / steps={steps} / {sampler} / {scheduler} / shift={shift} ")

            time.sleep(0.5)

print("✅ 전체 배치 완료")


#
# sampler_scheduler_list = [
#     # 🔥 Euler 계열
#     ("euler", "normal"),
#     ("euler_ancestral", "normal"),
#     ("euler_cfg_pp", "karras"),
#     ("euler_ancestral_cfg_pp", "karras"),
#
#     # 🔥 Heun 계열
#     ("heun", "normal"),
#     ("heunpp2", "karras"),
#
#     # 🔥 DPM 기본
#     ("dpm_2", "karras"),
#     ("dpm_2_ancestral", "karras"),
#     ("dpm_fast", "normal"),
#     ("dpm_adaptive", "normal"),
#
#     # 🔥 DPM++ 핵심 (가장 중요 ⭐)
#     ("dpmpp_2m", "karras"),
#     ("dpmpp_2m_cfg_pp", "karras"),
#     ("dpmpp_2m_sde", "karras"),
#     ("dpmpp_2m_sde_gpu", "karras"),
#
#     ("dpmpp_sde", "karras"),
#     ("dpmpp_sde_gpu", "karras"),
#
#     ("dpmpp_2s_ancestral", "karras"),
#     ("dpmpp_2s_ancestral_cfg_pp", "karras"),
#
#     ("dpmpp_3m_sde", "karras"),
#     ("dpmpp_3m_sde_gpu", "karras"),
#
#     # 🔥 기타 안정형
#     ("lms", "normal"),
#     ("ddim", "normal"),
#
#     # 🔥 최신/빠른 계열
#     ("uni_pc", "normal"),
#     ("uni_pc_bh2", "normal"),
#
#     # 🔥 특수 (속도/실험)
#     ("lcm", "normal"),
#     ("ipndm", "normal"),
#     ("ipndm_v", "normal"),
#     ("deis", "normal"),
#
#     # 🔥 res 계열
#     ("res_multistep", "karras"),
#     ("res_multistep_cfg_pp", "karras"),
#     ("res_multistep_ancestral", "karras"),
#     ("res_multistep_ancestral_cfg_pp", "karras"),
#
#     # 🔥 기타 실험용
#     ("gradient_estimation", "normal"),
#     ("gradient_estimation_cfg_pp", "karras"),
#     ("er_sde", "karras"),
#     ("sa_solver", "normal"),
#     ("sa_solver_pece", "normal"),
# ]