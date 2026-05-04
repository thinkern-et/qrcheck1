import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image

# 페이지 설정
st.set_page_config(page_title="QR 코드 일련번호 추출기", layout="wide")

st.title("🔍 QR 코드 실시간 추적 및 분석")
st.write("이미지를 업로드하면 시스템이 일련번호를 자동으로 역추적합니다.")

# 1. 파일 업로드 사이드바
uploaded_file = st.sidebar.file_uploader("QR 이미지 업로드", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # 2. 이미지 처리
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Streamlit 표시용

    # 3. QR 코드 디코딩
    decoded_objects = decode(img)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("업로드된 이미지")
        st.image(img_rgb, use_container_width=True)

    with col2:
        st.subheader("분석 결과")
        
        if not decoded_objects:
            st.warning("QR 코드를 찾을 수 없습니다. 이미지를 확인해주세요.")
        else:
            results = []
            display_img = img_rgb.copy()

            for obj in decoded_objects:
                qr_data = obj.data.decode('utf-8')
                qr_type = obj.type
                results.append({"타입": qr_type, "일련번호(Data)": qr_data})

                # 박스 그리기
                (x, y, w, h) = obj.rect
                cv2.rectangle(display_img, (x, y), (x + w, y + h), (0, 255, 0), 5)

            st.image(display_img, caption="인식된 QR 영역", use_container_width=True)
            
            # 결과 테이블 출력
            st.success(f"{len(decoded_objects)}개의 QR 코드를 발견했습니다.")
            st.table(results)

            # 코드 형태로도 확인하고 싶을 때
            with st.expander("원문 데이터(Raw Data) 보기"):
                st.code([r["일련번호(Data)"] for r in results])
else:
    st.info("왼쪽 사이드바에서 QR 코드 이미지를 업로드해주세요.")

# 하단에 코드 정보 표시 (선택 사항)
st.divider()
st.caption("Powered by Streamlit & PyZbar")
