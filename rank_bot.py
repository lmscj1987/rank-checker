import requests
from bs4 import BeautifulSoup

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 플레이스 검색 결과 페이지 (모바일 버전)
        url = f"https://m.search.naver.com/search.naver?query={keyword}&where=m_local"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://m.naver.com/'
        }
        
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 1. 개별 업체 정보가 담긴 '아이템 박스'들을 모두 가져옵니다.
        items = soup.select(".list_item_place, .UE719, .VL6S3")
        
        places = []
        for item in items:
            # [핵심] 광고 여부 체크: '광고' 배지나 클래스가 있으면 번호를 매기지 않고 건너뜁니다.
            is_ad = item.select_one(".ad_badge, .api_save_ad, .sp_local_ad")
            if is_ad:
                continue
            
            # 2. 광고가 아닌 경우에만 이름을 추출하여 리스트에 넣습니다.
            name_tag = item.select_one(".TYaxT, .place_name")
            if name_tag:
                name = name_tag.get_text().strip()
                if name and name not in places:
                    places.append(name)
        
        # 3. 순위 비교 (공백 무시)
        rank = 0
        target_clean = target_name.replace(" ", "")
        for idx, name in enumerate(places, 1):
            if target_clean in name.replace(" ", ""):
                rank = idx
                break
        
        if rank > 0:
            return f"{rank}위"
        else:
            return "40위권 밖"
            
    except Exception:
        return "데이터 분석 중"

if __name__ == "__main__":
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    # 실제 광고가 빠졌을 때 서초우물이 7위가 되는지 확인
    result_text = f"📢 [광고 필터링 최종 완료]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
