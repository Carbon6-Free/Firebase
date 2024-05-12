from firebase import firebase
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from crawler_module import *
from network_carborn import *
import random
import re

firebase=firebase.FirebaseApplication("https://(your url).firebaseio.com/",None)
    
chromedriver_path = './chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-web-security')  # CORS 정책 우회 설정
options.add_argument('--headless')

# CORS 정책 우회 설정
capabilities = DesiredCapabilities.CHROME.copy()
capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}

driver = webdriver.Chrome(service= Service(chromedriver_path), options=options)
content = []
data = []
cando = ["fetch", "css", "img", "script","link","video"]

def getjsonData(url):
    jsonData = []
    totSize = 0
    datasizeoftype = {"fetch":0, "css":0, "img":0, "script":0, "link":0, "video":0}
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        network_requests = driver.execute_script("return window.performance.getEntriesByType('resource');")

        for entry in network_requests:
            size = get_data_size(entry["name"])
            if (entry["initiatorType"] in cando):
                print(entry["name"], entry["responseStatus"], entry["initiatorType"], size, entry["duration"], sep="\n")
                totSize += size
                datasizeoftype[entry["initiatorType"]] += size
                jsonData.append({
                    "Name": entry["name"],
                    "Status": entry["responseStatus"],
                    "Type": entry["initiatorType"],
                    "Size": size,
                    "Time": entry["duration"]
                })
        content.append({
            "URL":url,
            "Contents":jsonData,
            "Size": totSize
        })

        return content, datasizeoftype
    except:
        pass
    
# Initialize session state for background color
if 'bg_color' not in st.session_state:
    st.session_state['bg_color'] = '#FFFFFF'  # Initial background color is black
if 'text_color' not in st.session_state:
    st.session_state['text_color'] = '#000000'  # Initial text color is white

# Page title
st.title("CarbonFree")

# Background color selection toggle
if st.toggle(':black-background[Black Background]', key='bg_checkbox'):
    st.session_state['bg_color'] = '#000000'
    st.session_state['text_color'] = '#FFFFFF'
else:
    st.session_state['bg_color'] = '#FFFFFF'
    st.session_state['text_color'] = '#000000'


# Apply background color and additional styles using CSS
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {st.session_state['bg_color']};
        }}
        .fixed-bottom-right {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: {st.session_state['bg_color']};
            color: {st.session_state['text_color']};
            border: 2px solid {st.session_state['text_color']};
            padding: 10px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
            width: 300px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Search term input text box
search_query = st.text_input(label='url', value='')  # Entered URL address

# Information list and random selection
info = [
    "난방온도 2℃ 낮추고 냉방온도 2℃ 높이기",
    "전기밥솥 보온기능 사용 줄이기",
    "냉장고 적정용량 유지하기",
    "비데 절전기능 사용하기",
    "물은 받아서 사용하기",
    "텔레비전 시청 시간 줄이기",
    "세탁기 사용횟수 줄이기",
    "디지털 탄소발자국 줄이기",
    "창틀과 문틈 바람막이 설치하기",
    "가전제품 대기전력 차단하기",
    "절수 설비 또는 절수 기기 설치하기",
    "고효율 가전제품 사용하기",
    "친환경 콘텐싱 보일러 사용하기",
    "주기적으로 보일러 청소하기",
    "LED 조명으로 교체하기",
    "가정 내 지역난방배관 청소하기",
    "음식물 쓰레기 줄이기",
    "저탄소 제품 구매하기",
    "저탄소 인증 농축산물 이용하기",
    "품질이 보증되고 오래 사용 가능한 제품 사기",
    "과대포장 제품 안 사기",
    "재활용하기 쉬운 재질·구조로 된 제품 구매하기",
    "우리나라, 우리 지역 식재료 이용하기",
    "개인용 자동차 대신 대중교통 이용하기",
    "친환경 운전 실천하기",
    "자동차 타이어 공기압과 휠 정기적으로 점검하기",
    "가까운 거리는 걷거나 자전거 이용하기",
    "전기·수소 자동차 구매하기",
    "재활용을 위한 분리배출 실천하기",
    "종이타월, 핸드드라이어 대신 개인손수건 사용하기",
    "장바구니 이용하고 비닐 사용 줄이기",
    "1회용 컵 대신 다회용 컵 사용하기",
    "물티슈 덜 쓰기",
    "음식 포장 시 1회용품 줄이기",
    "인쇄 시 종이 사용 줄이기",
    "청구서, 영수증 등의 전자적 제공 서비스 이용",
    "정부, 기업, 단체 등에서 추진하는 나무 심기 운동 참여하기",
    "탄소흡수원의 중요성을 알고 보호하기",
    "기념일에 내(가족) 나무 심어 보기"
]

selected_info = random.choice(info)
# Display the selected info in a styled box at the bottom right
st.markdown(
    f'<div class="fixed-bottom-right">{selected_info}</div>',
    unsafe_allow_html=True
)

# View results button
if st.button("View results"):
    log, datasize = getjsonData(search_query)
    datasize["g of CO2"] = annual_carborn(log[-1]["Size"])
    # Storing and retrieving data in Firebase
    match = re.search(r'(?<=://)(.*?)(?=/|$)', search_query)  # 도메인 이름 추출을 위한 정규표현식
    if match:
        domain = match.group(1)  # 도메인 이름 추출
        modified_domain = domain.replace(".", "-")  # '.'을 '-'로 변경
        print(modified_domain)

    firebase.post(f'{modified_domain}/', datasize)
    result = firebase.get(f'/{modified_domain}', '')

    # Output result
    for key, value in result.items():
        for sub_key, sub_value in value.items():
            st.write(f"{sub_key}: {sub_value}")
