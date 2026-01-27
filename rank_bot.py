import os
import requests
from bs4 import BeautifulSoup

# GitHub Secrets에서 가져온 보안 정보
token = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')

def get_ranking():
    """어제 성공했던 바로 그 크롤링 로직"""
    # 순위를 확인할 네이버 검색 주소
    url = "https://search.naver.com/search.naver?query=원하는키워드" 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # [핵심] 어제 순위를 정확히 짚어냈던 클래스명 (예: .lst_item 또는 .item_info)
        items = soup.select('.lst_item') 
        
        for i, item in enumerate(items, 1):
            if "본인업체명" in item.text: # 실제 업체명을 적어주세요
                return f"현재 {i}위입니다! 🎉"
        
        return "순위권 내에서 찾을 수 없습니다."

    except Exception as e:
        return f"크롤링 중 오류 발생: {e}"

def send_telegram(message):
    """텔레그램 메시지 전송"""
    if not token or not chat_id:
        print("에러: TELEGRAM_TOKEN 또는 CHAT_ID가 설정되지 않았습니다.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, json=payload)

if __name__ == "__main__":
    # 순위 계산 후 결과 전송
    rank_result = get_ranking()
    send_telegram(f"📊 [정기 순위 보고]\n{rank_result}")
