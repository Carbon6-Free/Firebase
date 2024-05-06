from firebase import firebase
import streamlit as st

firebase=firebase.FirebaseApplication("firebase 데이터베이스 링크 ",None)

st.title("CarbonFree")

# 검색어 입력을 받는 텍스트 상자
search_query = st.text_input(label='', value='url을 입력하세요')

# 엔터(입력 버튼)를 누르면 결과 표시
if st.button("결과보기"):

    data={
        'Carbon_Intensity': 450,
        'GPU_Info': 'macOS M3 GPU',
        'Memory_Usage': 0.219,
        'Power_Usage': 15.10000001,
        'Carbon_Grade': 'B'
    }   

    # Firebase에서 데이터 가져오기
    firebase.post(f'{search_query}/', data)
    result = firebase.get(f'/{search_query}','')

    
    # st.write(result)

    for key, value in result.items():
            #st.write(f"{key}:")
            for sub_key, sub_value in value.items():
                st.write(f"{sub_key}: {sub_value}")