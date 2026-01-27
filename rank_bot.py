import os
import requests
from bs4 import BeautifulSoup

# [보안] GitHub Secrets에서 값을 안전하게 가져옵니다.
token = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')

def get_ranking():
    """어제 만든 순위 크롤링 로직"""
    # 1. 대상 URL (어제 설정한 주소)
    url = "https://search.naver.com/search.naver?query=원하는키워드" 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. 순위 요소 찾기 (어제 사용한 태그와 클래스명)
        # 예: 검색 결과 리스트 가져오기
        items = soup.select('.item_info') # <-- 이 부분을 어제 성공했던 클래스명으로 확인하세요!
        
        rank = "순위권 밖"
        for i, item in enumerate(items):
            if "내업체명" in item.text: # <-- 본인의 업체명/상품명
                rank = f"현재 {i+1}위입니다! 🎉"
                break
        return rank

    except Exception as e:
        return f"순위 확인 중 오류 발생: {e}"

def send_telegram(message):
    """텔레그램 메시지 전송"""
    if not token or not chat_id:
        print("에러: 토큰 또는 CHAT_ID가 없습니다.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, json=payload)

if __name__ == "__main__":
    # 1. 순위 가져오기
    current_rank = get_ranking()
    
    # 2. 메시지 구성
    final_msg = f"📊 [데일리 순위 리포트]\n결과: {current_rank}"
    
    # 3. 전송
    send_telegram(final_msg)
    print("전송 완료!")
