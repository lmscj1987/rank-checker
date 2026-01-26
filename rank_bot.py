import os
import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_perfect_rank(keyword, target_name):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = f"https://map.naver.com/v5/search/{keyword}"
    driver.get(url)
    
    try:
        wait = WebDriverWait(driver, 15)
        # 지도 검색 결과 Iframe으로 전환
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "searchIframe")))
        
        # 스크롤 가능한 컨테이너 대기
        container = wait.until(EC.presence_of_element_located((By.ID, "_pcmap_list_scroll_container")))

        final_list = [] 
        seen_names = set() 

        # 스크롤 횟수를 25회로 늘려 약 50~60위까지 검색 (사당우물 누락 방지)
        for _ in range(25):
            items = driver.find_elements(By.CSS_SELECTOR, "li.UEzoS")
            for item in items:
                # 광고 필터링
                is_ad = item.find_elements(By.CSS_SELECTOR, ".sp_ad, .X0_67, .nmVf0, .p_ad")
                ad_text = item.find_elements(By.XPATH, ".//span[contains(text(), '광고')]")
                if is_ad or ad_text:
                    continue 

                try:
                    # 업체명 추출 (여러 클래스 대응)
                    name_element = item.find_element(By.CSS_SELECTOR, ".TYf9Z, .place_bluelink, .C6_yW")
                    name = name_element.text.strip()
                    if name and name not in seen_names:
                        seen_names.add(name)
                        final_list.append(name)
                except:
                    continue
            
            # 아래로 스크롤 (사당술집처럼 결과가 많은 키워드 대응)
            driver.execute_script("arguments[0].scrollBy(0, 3000)", container)
            time.sleep(1.2)

        driver.quit()

        # 순위 탐색 (공백 제거 후 비교하여 정확도 상승)
        clean_target = target_name.replace(" ", "")
        for i, name in enumerate(final_list):
            if clean_target in name.replace(" ", ""):
                return i + 1 
        return "순위권 밖"
    except Exception as e:
        if 'driver' in locals(): driver.quit()
        return f"확인불가(에러)"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': message})

if __name__ == "__main__":
    print(f"📡 {datetime.now().strftime('%Y-%m-%d %H:%M')} 순위 측정 시작")
    
    # 사당우물은 '사당술집', 서초우물은 '교대술집'으로 체크
    rank1 = get_perfect_rank("사당술집", "사당우물")
    rank2 = get_perfect_rank("교대술집", "서초우물")
    
    result_msg = (
        "📢 [순위 체크 완료]\n\n"
        f"📍 사당우물: {rank1}{'위' if isinstance(rank1, int) else ''}\n"
        f"📍 서초우물: {rank2}{'위' if isinstance(rank2, int) else ''}\n\n"
        "데이터를 기반으로 한 실시간 결과입니다! 🚀"
    )
    
    print(result_msg)
    send_telegram(result_msg)
