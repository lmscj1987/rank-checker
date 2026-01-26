import requests
from bs4 import BeautifulSoup
import os

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        url = f"https://search.naver.com/search.naver?query={keyword}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 검색 결과 텍스트 내에서 업체명의 위치를 찾습니다.
        # (이 방식은 가장 기초적인 텍스트 매칭 방식입니다)
        all_text = soup.get_text()
        
        if target_name in all_text:
            # 실제 순위 파싱 로직 (네이버 UI에 따라 변동될 수 있음)
            # 여기서는 예시로 접속 성공 메시지와 함께 포함 여부를 알립니다.
            return "순위권 진입 확인" 
        else:
            return "순위권 밖 (미검색)"
            
    except Exception as e:
        return f"오류 발생: {str(e)}"

if __name__ == "__main__":
    # 실제 체크
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [순위 체크 알림]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    # 로그 출력
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
