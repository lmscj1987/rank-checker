import requests
from bs4 import BeautifulSoup

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 1. 예전 코드 방식 그대로 모바일 검색 결과 활용
        url = f"https://m.search.naver.com/search.naver?query={keyword}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 2. 정확도가 높았던 플레이스 명칭 추출 로직 (주신 코드 그대로)
        # .place_name, .L_0S_, .name 세 가지 클래스를 우선 사용합니다.
        place_elements = soup.select(".place_name, .L_0S_, .name") 
        
        # 3. 중복 제거 및 순서 유지
        places = []
        for el in place_elements:
            name = el.get_text().strip()
            if name and name not in places:
                places.append(name)
        
        # 4. 순위 판별 (40위까지 보려면 검색 결과 리스트 전체를 돕니다)
        rank = 0
        for idx, name in enumerate(places, 1):
            # 띄어쓰기 무시하고 비교하는 정확한 로직
            if target_name.replace(" ", "") in name.replace(" ", ""):
                rank = idx
                break
        
        if rank > 0:
            return f"현재 {rank}위"
        else:
            return "순위권 밖"
            
    except Exception as e:
        return "분석 오류"

if __name__ == "__main__":
    # 타겟 업체명 확인
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [정확도 복구 완료]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
