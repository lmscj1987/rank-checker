import requests
from bs4 import BeautifulSoup

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 플레이스 탭 검색 결과 (50개까지 노출)
        url = f"https://m.search.naver.com/search.naver?query={keyword}&where=m_local"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://m.naver.com/'
        }
        
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 플레이스 리스트 아이템 추출
        items = soup.select(".list_item_place, .UE719, .VL6S3")
        
        places = []
        for item in items:
            # [필수] 광고(AD)는 순위 계산에서 완전히 제외
            if item.select_one(".ad_badge, .api_save_ad, .sp_local_ad"):
                continue
            
            # 업체명 추출
            name_tag = item.select_one(".TYaxT, .place_name")
            if name_tag:
                name = name_tag.get_text().strip()
                if name and name not in places:
                    places.append(name)
        
        # 순위 매칭
        rank = 0
        target_clean = target_name.replace(" ", "")
        for idx, name in enumerate(places, 1):
            if target_clean in name.replace(" ", ""):
                rank = idx
                break
        
        if rank > 0:
            return f"{rank}위"
        else:
            return "50위권 밖" # 광범위 키워드이므로 범위를 50위로 확장
            
    except Exception:
        return "데이터 분석 오류"

if __name__ == "__main__":
    # 요청하신 검색어와 타겟 업체 매칭
    # 1. '사당술집' 검색 시 '사당우물' 순위
    res1 = get_naver_rank('사당술집', '사당우물')
    
    # 2. '교대술집' 검색 시 '서초우물' 순위
    res2 = get_naver_rank('교대술집', '서초우물')
    
    result_text = f"📊 [플레이스 순위 리포트]\n\n🍺 사당술집 내 '사당우물': {res1}\n🍺 교대술집 내 '서초우물': {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
