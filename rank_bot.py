import requests
import re

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 봇 감지를 피하기 위해 실제 아이폰에서 검색하는 주소 형식을 사용합니다.
        url = f"https://m.search.naver.com/p/api/search.naver?where=m_local&query={keyword}&display=100&start=1"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://m.search.naver.com/'
        }
        
        res = requests.get(url, headers=headers, timeout=10)
        content = res.text

        # 1. 광고 업체 아이디들을 먼저 수집합니다 (순위 제외용)
        ad_ids = re.findall(r'\"adId\":\"(\d+)\"', content)
        
        # 2. 모든 업체 리스트를 가져옵니다.
        # "id":"123", "title":"업체명" 구조를 파싱합니다.
        items = re.findall(r'\"id\":\"(\d+)\".*?\"title\":\"([^"]+)\"', content)
        
        places = []
        for item_id, title in items:
            # 광고 아이디 리스트에 없는 '진짜' 업체만 순위에 포함시킵니다.
            if item_id not in ad_ids:
                # 불필요한 중복 제거
                if title not in places:
                    places.append(title)

        # 3. 내 업체 순위 매칭 (공백 무시)
        rank = 0
        target_clean = target_name.replace(" ", "")
        for idx, name in enumerate(places, 1):
            if target_clean in name.replace(" ", ""):
                rank = idx
                break
        
        if rank > 0:
            return f"{rank}위"
        else:
            return "100위권 밖"
            
    except Exception as e:
        return f"분석 에러"

if __name__ == "__main__":
    # 요청하신 검색어와 타겟 매칭
    res1 = get_naver_rank('사당술집', '사당우물')
    res2 = get_naver_rank('교대술집', '서초우물') # 실제 7위로 나오는지 확인 대상
    
    result_text = f"📊 [광고 제외 정밀 리포트]\n\n🍺 사당술집 내 '사당우물': {res1}\n🍺 교대술집 내 '서초
