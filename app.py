import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image

# 1. 페이지 레이아웃 설정
st.set_page_config(page_title="QR Serial Tracker", layout="centered")

st.title("🔍 QR 코드 일련번호 추출기")
st.markdown("이미지를 업로드하면 시스템이 자동으로 **일련번호**를 반환합니다.")

# 2. 파일 업로드 컴포넌트
uploaded_file = st.file_uploader("QR 이미지를 업로드하세요 (JPG, PNG, JPEG)", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # 이미지를 처리 가능한 형태로 변환
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    # OpenCV는 BGR을 사용하므로 변환 (필요한 경우)
    if len(img_array.shape) == 3:
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    else:
        img_cv = img_array

    # 3. QR 코드 디코딩
    decoded_objects = decode(img_cv)

    st.divider()

    if not decoded_objects:
        st.error("QR 코드를 인식하지 못했습니다. 사진의 화질이나 각도를 확인해주세요.")
    else:
        st.success(f"{len(decoded_objects)}개의 QR 코드가 발견되었습니다!")
        
        for idx, obj in enumerate(decoded_objects):
            # 일련번호 추출
            serial_number = obj.data.decode('utf-8')
            
            # 결과 표시 박스
            with st.container():
                st.subheader(f"결과 #{idx+1}")
                st.code(serial_number, language='text') # 복사하기 쉽게 코드 블록으로 표시
                
                # 이미지 상에 위치 표시 (시각화 선택 사항)
                (x, y, w, h) = obj.rect
                st.info(f"위치 정보: x={x}, y={y}, width={w}, height={h}")

    # 업로드한 이미지 미리보기
    with st.expander("원본 이미지 보기"):
        st.image(image, use_container_width=True)

else:
    st.info("파일을 기다리고 있습니다...")
