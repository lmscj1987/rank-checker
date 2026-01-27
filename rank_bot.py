import os
import requests
from bs4 import BeautifulSoup

# [보안] GitHub Secrets에서 안전하게 가져오는 설정
token = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')

def get_ranking():
    """어제 성공했던 바로 그 크롤링 로직"""
    # 어제 우리가 결과값을 잘 받아왔던 주소와 설정입니다.
    url = "https://search.naver.com/search.naver?query=원하는키워드" 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # [핵심] 어제 순위를 정확히 짚어냈던 태그 로직
        # 실제 네이버 쇼핑이나 광고 영역 등 어제 맞춘 클래스명을 그대로 사용합니다.
        items = soup.select('.lst_item') # 어제 성공한 태그로 고정!
        
        for i, item in enumerate(items, 1):
            if "본인업체명" in item.text: # 어제 찾았던 그 이름
                return f"현재 {i}위입니다! 🎉"
        
        return "순위권 내에서 찾을 수 없습니다."

    except Exception as e:
        return f"크롤링 중 오류 발생: {e}"

def send_telegram(message):
    """텔레그램 전송"""
    if not token or not chat_id:
        print("토큰이나 ID가 설정되지 않았습니다.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, json=payload)

if __name__ == "__main__":
    # 어제 작동했던 그 로직 그대로 실행
    rank_result = get_ranking()
    send_telegram(f"📊 실시간 순위 보고\n{rank_result}")
