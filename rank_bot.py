import os
import time
import requests
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_perfect_rank(keyword, target_name):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = f"https://map.naver.com/v5/search/{keyword}"
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "searchIframe")))
        container = wait.until(EC.presence_of_element_located((By.ID, "_pcmap_list_scroll_container")))

        final_list = [] 
        seen_names = set() 

        for _ in range(20):
            items = driver.find_elements(By.CSS_SELECTOR, "li.UEzoS")
            for item in items:
                # 광고 필터링
                is_ad = item.find_elements(By.CSS_SELECTOR, ".sp_ad, .X0_67, .nmVf0, .p_ad")
                ad_text = item.find_elements(By.XPATH, ".//span[contains(text(), '광고')]")
                if is_ad or ad_text: continue 

                try:
                    name = item.find_element(By.CSS_SELECTOR, ".TYf9Z, .place_bluelink").text.strip()
                    if name not in seen_names:
                        seen_names.add(name)
                        final_list.append(name)
                except: continue
            
            driver.execute_script("arguments[0].scrollBy(0, 3000)", container)
            time.sleep(1.5)

        driver.quit()
        for i, name in enumerate(final_list):
            if target_name in name: return i + 1 
        return "순위권 밖"
    except:
        if 'driver' in locals(): driver.quit()
        return "에러"

def run_task():
    token = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
    chat_id = "8479493770"
    
    targets = [{"kw": "사당술집", "nm": "사당우물"}, {"kw": "교대술집", "nm": "서초우물"}]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    results = []
    
    for t in targets:
        rank = get_perfect_rank(t['kw'], t['nm'])
        results.append(rank)

    # 엑셀 저장
    file_name = "플레이스_순위_통합기록.xlsx"
    df_new = pd.DataFrame([{"날짜": now, "사당우물": results[0], "서초우물": results[1]}])
    if os.path.exists(file_name):
        df_old = pd.read_excel(file_name)
        df_new = pd.concat([df_old, df_new], ignore_index=True)
    df_new.to_excel(file_name, index=False)

    # 텔레그램 전송
    msg = f"📢 [순위 알림]\n\n📍 사당우물: {results[0]}위\n📍 서초우물: {results[1]}위\n\n⏰ {now}"
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={'chat_id': chat_id, 'text': msg})

if __name__ == "__main__":
    run_task()
