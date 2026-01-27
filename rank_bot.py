import requests
from bs4 import BeautifulSoup

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 40위권까지 보기 위해 플레이스 전체 리스트 URL 활용
        # m.search.naver.com 대신 n.search.naver.com의 플레이스 영역을 타겟팅합니다.
        url = f"https://m.search.naver.com/search.naver?query={keyword}&where=m_local"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 플레이스 리스트 내의 업체명 클래스 (TYaxT는 네이버 플레이스의 주요 업체명 클래스입니다)
        # 40위권까지 데이터가 로드되도록 선택자를 구성합니다.
        place_elements = soup.select(".TYaxT, .place_name, .L_0S_") 
        
        places = []
        for el in place_elements:
            name = el.get_text().strip()
            if name and name not in places:
                places.append(name)
        
        rank = 0
        target_name_clean = target_name.replace(" ", "")
        
        # 최대 50개까지만 검사 (네이버가 한 번에 내려주는 리스트 양에 따름)
        for idx, name in enumerate(places, 1):
            if target_name_clean in name.replace(" ", ""):
                rank = idx
                break
        
        if rank > 0:
            return f"현재 {rank}위"
        else:
            # 40위권 밖인 경우에 대한 메시지
            return "40위권 밖"
            
    except Exception as e:
        print(f"오류 내용: {e}")
        return "분석 오류"

if __name__ == "__main__":
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [정확도 및 범위 개선 알림]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
