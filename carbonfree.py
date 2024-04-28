from firebase import firebase
import streamlit as st

firebase=firebase.FirebaseApplication("myurl",None)

st.title("CarbonFree")

# 검색어 입력을 받는 텍스트 상자
search_query = st.text_input(label='', value='url을 입력하세요')

# 엔터(입력 버튼)를 누르면 결과 표시
if st.button("결과보기"):

    data={
        'Carbon_Intensity': 443,
        'GPU_Info': 'macOS M2 GPU',
        'Memory_Usage': 0.219,
        'Power_Usage': 15.10000001,
        'Carbon_Grade': 'C'
    }   
    
    result = firebase.post(f'/{search_query}',data)

    # Firebase에서 데이터 가져오기
    #fetched_data = firebase.get(f'\{search_query}', data)
    #if fetched_data:

    st.write("Carbon_Intensity:", result.get('Carbon_Intensity'))
    st.write("GPU_Info:", result.get('GPU_Info'))
    st.write("Memory_Usage:", result.get('Memory_Usage'))
    st.write("Power_Usage:", result.get('Power_Usage'))
    st.write("Carbon_Grade:", result.get('Carbon_Grade'))



