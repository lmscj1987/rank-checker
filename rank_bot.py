import requests
from bs4 import BeautifulSoup

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 네이버 플레이스 검색 결과 위주로 분석하기 위해 모바일 경로 사용
        url = f"https://m.search.naver.com/search.naver?query={keyword}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36'
        }
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 플레이스 리스트 내의 업체명 태그들을 수집
        # 네이버 구조 변경에 따라 클래스명은 유동적일 수 있으나 현재 주로 쓰이는 태그를 타겟팅합니다.
        places = soup.select(".place_name, .name, .L_0S_") 
        
        rank = 0
        found = False
        
        for idx, place in enumerate(places, 1):
            if target_name in place.get_text():
                rank = idx
                found = True
                break
        
        if found:
            return f"현재 {rank}위"
        else:
            return "20위권 밖 (미검색)"
            
    except Exception as e:
        return f"오류 발생: {str(e)}"

if __name__ == "__main__":
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [실시간 순위 알림]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
