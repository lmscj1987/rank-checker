import requests
from bs4 import BeautifulSoup

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 플레이스 검색 리스트를 직접 호출하여 순위 정확도 확보
        url = f"https://m.search.naver.com/search.naver?query={keyword}&where=m_local"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
        }
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 1. 광고 업체 제외 로직: 광고는 보통 'sp_local_ad' 클래스를 포함합니다.
        # 2. 업체명 추출: 현재 가장 정확한 태그인 .TYaxT를 기반으로 추출
        items = soup.select(".list_item_place, .UE719") # 플레이스 개별 아이템 박스
        
        places = []
        for item in items:
            # 광고 뱃지가 있는지 확인하여 광고는 순위에서 제외
            is_ad = item.select_one(".api_save_ad, .ad_badge")
            if is_ad:
                continue
            
            # 업체명 찾기
            name_tag = item.select_one(".TYaxT, .place_name")
            if name_tag:
                name = name_tag.get_text().strip()
                if name not in places:
                    places.append(name)

        # 실제 순위 계산 (공백 제거 비교)
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
        return "분석 오류"

if __name__ == "__main__":
    # 점검 결과: 서초우물 7위 반영 확인용
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [실시간 순위 보고]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
