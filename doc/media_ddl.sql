-- SUBJECT
gender, nationality, body_type, skin_tone,
hair_length, hair_color, hair_style,
makeup_style,

-- OUTFIT
outfit_type, outfit_style, outfit_color,
outfit_material, outfit_fit, outfit_detail,
shoes, accessories,

-- ACTION
pose, action, expression, mood, gaze,

-- ENV
location, background, time, weather,

-- LIGHT
lighting_type, light_direction, light_intensity, shadow_style,

-- CAMERA
shot, camera_angle, lens,

-- STYLE
rendering_style, color_grading, resolution





의상 taxonomy는 이렇게 나눠야 합니다:

WHAT  → 무엇을 입었나 (type)
HOW   → 어떻게 생겼나 (style/fit/detail)
LOOK  → 시각적 요소 (color/material)
STATE → 노출/상태 (exposure)
CONTEXT → 상황/용도 (scene)

👉 이 5축 구조가 가장 안정적입니다.

✅ 2. 추천 DB 구조 (실전용)
outfit_type TEXT,        -- dress, swimwear, suit, lingerie
outfit_category TEXT,    -- casual, formal, sport, beach

outfit_style TEXT,       -- sleeveless, off-shoulder, tight, oversized
outfit_fit TEXT,         -- slim fit, loose fit, bodycon

outfit_color TEXT,       -- red, black, pastel pink
outfit_material TEXT,    -- cotton, silk, leather, denim

outfit_detail TEXT,      -- lace, frill, zipper, cutout

exposure_level TEXT,     -- fully_clothed, partial, revealing, nude
body_focus TEXT,         -- legs, chest, waist, full body

scene_type TEXT,         -- beach, studio, street, indoor





-- powershell ssh root@onechart.iptime.org
-- su - postgres
-- psql postgres
-- CREATE USER media WITH ENCRYPTED PASSWORD 'm1234';
-- CREATE DATABASE media OWNER media;
-- GRANT ALL PRIVILEGES ON DATABASE media TO media;


CREATE TABLE images (
    id UUID PRIMARY KEY,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    name TEXT,
    job_category TEXT,
    job TEXT,
    action TEXT,
    pose TEXT,
    emotion TEXT,
    tags TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- 기본
CREATE INDEX idx_images_created_at ON images (created_at DESC);

-- 필터
CREATE INDEX idx_images_job_category ON images (job_category);

-- 배열
CREATE INDEX idx_images_tags_gin ON images USING GIN (tags);

-- JSON
CREATE INDEX idx_images_metadata_gin ON images USING GIN (metadata);

-- 복합
CREATE INDEX idx_images_category_created ON images (job_category, created_at DESC);










CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE prompt_profiles_flat (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- 기본 정보
    name TEXT,
    gender TEXT,
    age INT,
    nationality TEXT,
    job TEXT,
    role TEXT,
    affiliation TEXT,

    -- 외형 (Appearance)
    face_shape TEXT,
    eye_color TEXT,
    eyebrow_style TEXT,
    nose_shape TEXT,
    lips TEXT,
    skin_tone TEXT,
    body_type TEXT,
    height INT,

    hair_length TEXT,
    hair_color TEXT,
    hair_style TEXT,
    bangs TEXT,

    makeup_style TEXT,
    makeup_detail TEXT,

    -- 의상 (Outfit)
    outfit_type TEXT,
    outfit_style TEXT,
    outfit_color TEXT,
    outfit_material TEXT,
    outfit_fit TEXT,
    outfit_detail TEXT,
    shoes TEXT,
    accessories TEXT,

    -- 환경 (Environment)
    location TEXT,
    background TEXT,
    environment_scale TEXT,
    surface_detail TEXT,
    time TEXT,
    weather TEXT,
    depth_of_field TEXT,

    -- 동작 (Action)
    pose TEXT,
    action TEXT,
    motion_type TEXT,
    gaze TEXT,

    -- 감정 (Emotion)
    expression TEXT,
    emotion TEXT,
    mood TEXT,
    situation TEXT,
    tension_level TEXT,

    -- 카메라 (Camera)
    shot TEXT,
    camera_angle TEXT,
    lens TEXT,
    focus TEXT,

    -- 조명 (Lighting)
    lighting_type TEXT,
    light_direction TEXT,
    light_intensity TEXT,
    shadow_style TEXT,
    rim_light TEXT,

    -- 효과 (Effects)
    hair_motion TEXT,
    cloth_motion TEXT,
    sweat TEXT,
    dust_particles TEXT,

    -- 스타일 (Style)
    rendering_style TEXT,
    color_grading TEXT,
    contrast TEXT,
    sharpness TEXT,
    grain TEXT,

    -- 품질 (Quality)
    resolution TEXT,
    detail_level TEXT,
    realism_level TEXT,

    extra JSONB,
    tags TEXT[],
    model TEXT,
    prompt_text TEXT,
  
    -- 네거티브
    negative_prompt TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE compy_workflow (
    name TEXT NOT NULL,
    description TEXT,
    workflow JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (name)
);


select * from compy_workflow;
