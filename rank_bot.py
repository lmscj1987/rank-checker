import requests
from bs4 import BeautifulSoup

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 플레이스 검색 결과 페이지 호출
        url = f"https://m.search.naver.com/search.naver?query={keyword}&where=m_local"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
        }
        
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 1. 모든 플레이스 아이템 박스를 순서대로 가져옴
        # 이 박스들 안에 광고 여부와 이름이 모두 들어있습니다.
        items = soup.select(".list_item_place, .UE719, .VL6S3")
        
        places = []
        for item in items:
            # [광고 필터링] 광고 배지나 태그가 포함되어 있다면 순위에서 과감히 제외
            if item.select_one(".ad_badge, .api_save_ad, .sp_local_ad"):
                continue
            
            # [이름 추출] 광고가 아닌 아이템에서만 이름을 추출
            name_tag = item.select_one(".TYaxT, .place_name")
            if name_tag:
                name = name_tag.get_text().strip()
                if name and name not in places:
                    places.append(name)
        
        # 순위 비교 (공백 무시)
        rank = 0
        target_clean = target_name.replace(" ", "")
        for idx, name in enumerate(places, 1):
            if target_clean in name.replace(" ", ""):
                rank = idx
                break
        
        if rank > 0:
