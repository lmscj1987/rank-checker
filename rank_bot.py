import requests
import re

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 네이버 모바일 플레이스 전용 API (가장 최신 보안 우회 방식)
        url = f"https://m.search.naver.com/p/api/search.naver?where=m_local&query={keyword}&display=50&start=1"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
            'Referer': 'https://m.search.naver.com/',
            'Accept': '*/*',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        # 세션을 사용하여 연결 유지 (차단 확률 감소)
        session = requests.Session()
        res = session.get(url, headers=headers, timeout=10)
        content = res.text

        # 1. 데이터 추출 (정규식으로 업체명만 쏙 뽑아내기)
        # 광고 데이터는 보통 이 API 응답의 'items' 리스트에 포함되지 않거나 별도로 표시됩니다.
        places = re.findall(r'\"title\":\"([^"]+)\"', content)
        
        # 불필요한 단어 필터링
        filtered_places = []
        exclude = ['지도', '전화', '검색', '공유', '길찾기', '이미지', '플레이스', '네이버', '더보기', '광고']
        for p in places:
            if p not in exclude and len(p) > 1:
                if p not in filtered_places:
                    filtered_places.append(p)

        # 2. 순위 비교
        rank = 0
        target_clean = target_name.replace(" ", "")
        for idx, name in enumerate(filtered_places, 1):
            if target_clean in name.replace(" ", ""):
                rank = idx
                break
        
        if rank > 0:
            return f"{rank}위"
        else:
            return "40위권 밖"
            
    except Exception:
        return "접속 장애"

if __name__ == "__main__":
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [차단 우회 성공 여부 점검]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
