import streamlit as st
from PIL import Image

st.title("메인 타이틀")

# Initialization of session state variables
if "language" not in st.session_state:
    st.session_state.language = "Python"  # st.radio 위젯이 기본값 저장
if "category" not in st.session_state:
    st.session_state.category = "Pixel Level"  # st.radio 위젯이 기본값 저장
if "language_confirmed" not in st.session_state:
    st.session_state.language_confirmed = False
if "category_confirmed" not in st.session_state:
    st.session_state.category_confirmed = False

# Uploaded files
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
        
        # 1단계: 개발 언어 선택 (초기 단계)
        if not st.session_state.language_confirmed:
            selected_language = st.radio("개발 언어 선택", ["Python", "C++"])
            if st.button("개발 언어 확인"):
                st.session_state.language_confirmed = True
                st.session_state.language = selected_language
                st.experimental_rerun()
        else:
            st.write("선택된 개발 언어:", st.session_state.language)
        
        # 2단계: 카테고리 선택 (개발 언어 선택 후에 표시)
        if st.session_state.get("language_confirmed"):
            if not st.session_state.category_confirmed:
                selected_categori = st.radio("카테고리 선택", ["Pixel Level", "Spatial Level"])
                if st.button("카테고리 확인"):
                    st.session_state.category_confirmed = True
                    st.session_state.category = selected_categori
                    st.experimental_rerun()
            else:
                st.write("선택된 카테고리:", st.session_state.category)
        
        # 3단계: 기능 토글 (언어 선택 + 카테고리 선택 후 표시)
        if st.session_state.get("language_confirmed") and st.session_state.get("category_confirmed"):
            if st.session_state.language == "Python":
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
            
        # 옵션 리셋 버튼 추가: "이전 옵션"은 카테고리 단계로, "처음 옵션"은 언어 선택 단계로 돌아갑니다.
        st.markdown("---")
        col_reset_prev, col_reset_initial = st.columns(2)
        if col_reset_prev.button("이전 옵션으로 돌아가기"):
            st.session_state.category_confirmed = False  # 카테고리부터 이후 단계 리셋
            st.experimental_rerun()
        if col_reset_initial.button("처음 옵션으로 돌아가기"):
            st.session_state.language_confirmed = False
            st.session_state.category_confirmed = False
            st.experimental_rerun()

    # 메인 영역: 이미지 표시
    try:
        from PIL import Image
        current_file = image_files[st.session_state.index]
        image = Image.open(current_file)
        st.image(image, caption="")
    except Exception as e:
        st.error(f"이미지를 불러오지 못했습니다: {e}")

    # 영상 아래쪽에 가운데 정렬된 이전/다음 버튼 배치 (메인 영역)
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        btn_prev, btn_next = st.columns(2)
        if btn_prev.button("이전"):
            st.session_state.index = (st.session_state.index - 1) % len(image_files)
        if btn_next.button("다음"):
            st.session_state.index = (st.session_state.index + 1) % len(image_files)
else:
    st.info("이미지 파일을 선택해주세요.")