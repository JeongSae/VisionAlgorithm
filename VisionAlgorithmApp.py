import streamlit as st
from PIL import Image

st.title("영상 처리 알고리즘 테스트")

# 이미지 파일 업로더 (여러 파일 선택 가능)
uploaded_files = st.file_uploader("이미지 파일을 선택하세요", type=["png", "jpg", "jpeg", "bmp", "gif"], accept_multiple_files=True)

if uploaded_files:
    # 업로드된 파일 목록
    image_files = list(uploaded_files)
    
    # 세션 상태를 이용해 현재 인덱스 관리
    if "index" not in st.session_state:
        st.session_state.index = 0

    # 왼쪽 사이드바에 영상 처리 옵션 및 내비게이션 컨트롤을 배치
    with st.sidebar:
        st.header("컨트롤 패널")
        # 이전/다음 버튼 (세로로 배치)
        if st.button("이전"):
            st.session_state.index = (st.session_state.index - 1) % len(image_files)
        if st.button("다음"):
            st.session_state.index = (st.session_state.index + 1) % len(image_files)
            
        st.markdown("---")
        st.subheader("영상 처리 옵션")
        # threshold 값 지정 슬라이더
        threshold_value = st.slider("Threshold 값", min_value=0, max_value=255, value=128)
        # crop 영역 크기 입력
        st.markdown("Crop 영역 (가로 x 세로)")
        crop_width = st.number_input("가로", min_value=1, value=100)
        crop_height = st.number_input("세로", min_value=1, value=100)
        st.markdown("---")
        st.subheader("기능 버튼")
        if st.button("기능 1"):
            st.info("기능 1 실행 예정")
        if st.button("기능 2"):
            st.info("기능 2 실행 예정")
        if st.button("기능 3"):
            st.info("기능 3 실행 예정")
    
    # 메인 영역에서는 이미지 표시
    current_file = image_files[st.session_state.index]
    try:
        image = Image.open(current_file)
        st.image(image, caption="")  # 파일 제목은 표시하지 않음.
    except Exception as e:
        st.error(f"이미지를 불러오지 못했습니다: {e}")
else:
    st.info("이미지 파일을 선택해주세요.")