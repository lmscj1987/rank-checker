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
    # 깃허브 액션(리눅스) 환경을 위한 필수 설정
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    # 드라이버 자동 설치 및 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = f"https://map.naver.com/v5/search/{keyword}"
    driver.get(url)
    
    try:
        wait = WebDriverWait(driver, 15)
        # 지도 검색 결과 Iframe으로 전환
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "searchIframe")))
        container = wait.until(EC.presence_of_element_located((By.ID, "_pcmap_list_scroll_container")))

        final_list = [] 
        seen_names = set() 

        # 스크롤하며 데이터 수집 (깃허브 사양에 맞춰 15회로 조정)
        for _ in range(15):
            items = driver.find_elements(By.CSS_SELECTOR, "li.UEzoS")
            for item in items:
                # 광고 필터링
                is_ad = item.find_elements(By.CSS_SELECTOR, ".sp_ad, .X0_67, .nmVf0, .p_ad")
                ad_text = item.find_elements(By.XPATH, ".//span[contains(text(), '광고')]")
                if is_ad or ad_text:
                    continue 

                try:
                    name = item.find_element(By.CSS_SELECTOR, ".TYf9Z, .place_bluelink").text.strip()
                    if name not in seen_names:
                        seen_names.add(name)
                        final_list.append(name)
                except:
                    continue
            
            driver.execute_script("arguments[0].scrollBy(0, 2000)", container)
            time.sleep(1.0)

        driver.quit()

        # 순위 탐색
        for i, name in enumerate(final_list):
            if target_name in name:
                return i + 1 
        return "순위권 밖"
    except Exception as e:
        if 'driver' in locals(): driver.quit()
        return f"에러: {str(e)}"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': message})

if __name__ == "__main__":
    print(f"📡 {datetime.now().strftime('%Y-%m-%d %H:%M')} 순위 측정 시작")
    
    # 전달주신 키워드로 체크
    rank1 = get_perfect_rank("사당술집", "사당우물")
    rank2 = get_perfect_rank("교대술집", "서초우물")
    
    result_msg = (
        "📢 [정확도 모드 순위 알림]\n\n"
        f"📍 사당우물: {rank1}{'위' if isinstance(rank1, int) else ''}\n"
        f"📍 서초우물: {rank2}{'위' if isinstance(rank2, int) else ''}\n\n"
        "오늘도 번창하세요! 🔥"
    )
    
    print(result_msg)
    send_telegram(result_msg)
