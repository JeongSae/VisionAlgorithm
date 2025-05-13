import streamlit as st
from PIL import Image
import numpy as np
from AlgorithmPython import ImageCrop
from streamlit_drawable_canvas import st_canvas

st.title("메인 타이틀")

# Session State 기본값 초기화
if "language" not in st.session_state:
    st.session_state.language = "Python"  # 기본값
if "category" not in st.session_state:
    st.session_state.category = "Pixel Level"  # 기본값
if "language_confirmed" not in st.session_state:
    st.session_state.language_confirmed = False
if "category_confirmed" not in st.session_state:
    st.session_state.category_confirmed = False
if "crop_mode" not in st.session_state:
    st.session_state.crop_mode = False

# 이미지 업로드
uploaded_files = st.file_uploader(
    "이미지 파일을 선택하세요",
    type=["png", "jpg", "jpeg", "bmp", "gif"],
    accept_multiple_files=True
)

if uploaded_files:
    image_files = list(uploaded_files)
    if "index" not in st.session_state:
        st.session_state.index = 0

    with st.sidebar:
        st.header("Vision Algorithm Options")
        st.markdown("---")
        st.subheader("기능 선택")
        
        # 1단계: 개발 언어 선택 (키 없이 st.radio 사용)
        if not st.session_state.language_confirmed:
            selected_language = st.radio("개발 언어 선택", ["Python", "C++"])
            if st.button("개발 언어 확인"):
                st.session_state.language_confirmed = True
                st.session_state.language = selected_language
                st.experimental_rerun()
        else:
            st.write("선택된 개발 언어:", st.session_state.language)
        
        # 2단계: 카테고리 선택 (키 없이)
        if st.session_state.language_confirmed:
            if not st.session_state.category_confirmed:
                selected_category = st.radio("카테고리 선택", ["Pixel Level", "Spatial Level"])
                if st.button("카테고리 확인"):
                    st.session_state.category_confirmed = True
                    st.session_state.category = selected_category
                    st.experimental_rerun()
            else:
                st.write("선택된 카테고리:", st.session_state.category)
        
        # 3단계: 기능 토글
        if st.session_state.language_confirmed and st.session_state.category_confirmed:
            if st.session_state.language == "Python":
                if st.session_state.category == "Pixel Level":
                    st.markdown("**Pixel Level 기능**")
                    pixel_functions = ["기능 1", "기능 2", "기능 3"]
                    selected_pixel = [func for func in pixel_functions if st.checkbox(func)]
                    if st.button("실행 Pixel Level"):
                        st.info(f"Pixel Level 기능 실행 예정: {selected_pixel}")
                elif st.session_state.category == "Spatial Level":
                    st.markdown("**Spatial Level 기능**")
                    spatial_functions = ["Cropping", "Resizing", "Rotating"]
                    selected_spatial = [func for func in spatial_functions if st.checkbox(func)]
                    if st.button("실행 Spatial Level"):
                        # 만약 Cropping 기능이 선택되었다면 crop_mode 플래그를 활성화
                        if "Cropping" in selected_spatial:
                            st.session_state.crop_mode = True
                        else:
                            st.info(f"Spatial Level 기능 실행 예정: {selected_spatial}")
            elif st.session_state.language == "C++":
                if st.session_state.category == "Pixel Level":
                    st.markdown("**Pixel Level 기능**")
                    pixel_functions = ["기능 1", "기능 2", "기능 3"]
                    selected_pixel = [func for func in pixel_functions if st.checkbox(func)]
                    if st.button("실행 Pixel Level"):
                        st.info(f"Pixel Level 기능 실행 예정: {selected_pixel}")
                elif st.session_state.category == "Spatial Level":
                    st.markdown("**Spatial Level 기능**")
                    spatial_functions = ["기능 A", "기능 B", "기능 C"]
                    selected_spatial = [func for func in spatial_functions if st.checkbox(func)]
                    if st.button("실행 Spatial Level"):
                        st.info(f"Spatial Level 기능 실행 예정: {selected_spatial}")
                        
        # 옵션 리셋 버튼 (이전 옵션: 카테고리 선택 단계, 처음 옵션: 개발 언어 단계)
        st.markdown("---")
        col_reset_prev, col_reset_initial = st.columns(2)
        if col_reset_prev.button("이전 옵션으로 돌아가기"):
            st.session_state.category_confirmed = False
            st.experimental_rerun()
        if col_reset_initial.button("처음 옵션으로 돌아가기"):
            st.session_state.language_confirmed = False
            st.session_state.category_confirmed = False
            st.experimental_rerun()
    
    # 메인 영역: 원본 이미지 로드
    try:
        current_file = image_files[st.session_state.index]
        original_image = Image.open(current_file).convert("RGB")
    except Exception as e:
        st.error(f"이미지를 불러오지 못했습니다: {e}")
    
    # 메인 영역: Crop 모드 (cropping 기능이 활성화된 경우)
    if st.session_state.crop_mode:
        st.subheader("크롭 영역 지정")
        st.write("사각형 드로잉 도구를 사용하여 크롭 영역을 지정하세요.")
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=3,
            stroke_color="#ff0000",
            background_image=original_image,
            update_streamlit=True,
            height=original_image.size[1],
            width=original_image.size[0],
            drawing_mode="rect"
        )
        if canvas_result.json_data is not None:
            objects = canvas_result.json_data.get("objects", [])
            if objects:
                # 첫 번째로 그린 사각형 영역 사용
                shape = objects[0]
                left = shape.get("left")
                top = shape.get("top")
                width = shape.get("width")
                height = shape.get("height")
                crop_area = (left, top, left + width, top + height)
                print(f"Crop Area: {crop_area}")
                cropped_image = ImageCrop.ImageCrop(original_image, crop_area)
                st.write("Before / After 크롭 결과:")
                col1, col2 = st.columns(2)
                with col1:
                    st.image(original_image, caption="Before")
                with col2:
                    st.image(cropped_image, caption="After")
            else:
                st.info("드래그하여 크롭할 영역을 지정해주세요.")
        if st.button("크롭 완료"):
            st.session_state.crop_mode = False
            st.experimental_rerun()
    
    # 메인 영역: 이전/다음 이미지 네비게이션 (하단)
    col_left, col_center, col_right = st.columns([1,2,1])
    with col_center:
        btn_prev, btn_next = st.columns(2)
        if btn_prev.button("이전"):
            st.session_state.index = (st.session_state.index - 1) % len(image_files)
        if btn_next.button("다음"):
            st.session_state.index = (st.session_state.index + 1) % len(image_files)
else:
    st.info("이미지 파일을 선택해주세요.")