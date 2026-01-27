import requests
from bs4 import BeautifulSoup

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 정확도가 높았던 모바일 검색 주소
        url = f"https://m.search.naver.com/search.naver?query={keyword}&where=m_local"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 모든 플레이스 아이템을 가져옵니다.
        items = soup.select(".list_item_place, .UE719, .VL6S3") 
        
        places = []
        for item in items:
            # [중요] 광고(AD) 요소가 포함되어 있으면 순위에서 제외합니다.
            if item.select_one(".ad_badge, .api_save_ad, .sp_local_ad"):
                continue
                
            # 업체명 추출 (주신 코드의 선택자 활용)
            name_tag = item.select_one(".place_name, .TYaxT, .name")
            if name_tag:
                name = name_tag.get_text().strip()
                if name and name not in places:
                    places.append(name)
        
        rank = 0
        target_clean = target_name.replace(" ", "")
        for idx, name in enumerate(places, 1):
            if target_clean in name.replace(" ", ""):
                rank = idx
                break
        
        if rank > 0:
            return f"현재 {rank}위"
        else:
            return "40위권 밖"
            
    except Exception as e:
        print(f"Error: {e}")
        return "분석 오류"

if __name__ == "__main__":
    # 사당우물, 서초우물 체크
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [순위 정밀 체크]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
