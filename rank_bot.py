import requests
from bs4 import BeautifulSoup

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 모바일 통합 검색 결과 (차단 저항력이 가장 강함)
        url = f"https://m.search.naver.com/search.naver?query={keyword}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
        }
        
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 네이버 플레이스 리스트 아이템 추출
        # 광고와 일반 업체를 구분하기 위해 아이템 박스를 먼저 잡습니다.
        items = soup.select(".list_item_place, .UE719, .VL6S3")
        
        places = []
        for item in items:
            # 1. 광고(AD) 태그가 있는지 확인 (있으면 순위에서 제외)
            if item.select_one(".ad_badge, .api_save_ad, .sp_local_ad"):
                continue
            
            # 2. 업체명 추출 (TYaxT는 현재 네이버의 표준 클래스입니다)
            name_tag = item.select_one(".TYaxT, .place_name")
            if name_tag:
                name = name_tag.get_text().strip()
                if name and name not in places:
                    places.append(name)
        
        # 디버깅용 로그: 실제로 몇 개의 업체를 찾았는지 출력
        print(f"[{keyword}] 수집된 업체 수: {len(places)}")

        # 순위 비교 (공백 무시)
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
        # 구체적인 에러 메시지를 출력하여 어디서 막혔는지 파악
        print(f"에러 발생: {e}")
        return "분석 오류"

if __name__ == "__main__":
    # 사당우물, 서초우물 순위 체크
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [최종 검증 완료 순위]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
