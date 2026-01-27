import requests
from bs4 import BeautifulSoup

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 주신 코드의 모바일 검색 방식 유지 (40위까지 나오도록 where=m_local 적용)
        url = f"https://m.search.naver.com/search.naver?query={keyword}&where=m_local"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # [핵심] 주신 코드에서 가장 정확했던 선택자만 사용
        place_elements = soup.select(".place_name, .L_0S_, .name, .TYaxT") 
        
        # 중복 제거 및 순서 유지
        places = []
        for el in place_elements:
            name = el.get_text().strip()
            if name and name not in places:
                places.append(name)
        
        # 순위 계산 (띄어쓰기 무시 로직 포함)
        rank = 0
        target_name_clean = target_name.replace(" ", "")
        for idx, name in enumerate(places, 1):
            if target_name_clean in name.replace(" ", ""):
                rank = idx
                break
        
        if rank > 0:
            return f"현재 {rank}위"
        else:
            return "40위권 밖"
            
    except Exception as e:
        return "분석 오류"

if __name__ == "__main__":
    # 키워드와 업체명 설정
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [순위 확인 알림]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
