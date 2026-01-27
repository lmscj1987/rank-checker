import requests
from bs4 import BeautifulSoup
import time

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 네이버 모바일 '플레이스' 탭 리스트를 직접 호출
        url = f"https://m.search.naver.com/search.naver?query={keyword}&where=m_local&sm=mtp_hty"
        
        # 실제 브라우저처럼 보이기 위한 고도화된 헤더 설정
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://m.naver.com/',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        # 3회 시도 (네이버의 일시적 차단 대비)
        for _ in range(3):
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                break
            time.sleep(1)
            
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 모든 플레이스 아이템 수집
        # .list_item_place 또는 .UE719가 개별 업체 박스입니다.
        items = soup.select(".list_item_place, .UE719, .VL6S3")
        
        places = []
        for item in items:
            # 1. 광고 업체 완전히 걸러내기
            if item.select_one(".ad_badge, .api_save_ad, .sp_local_ad"):
                continue
                
            # 2. 업체명 추출 (.TYaxT가 현재 가장 정확함)
            name_tag = item.select_one(".TYaxT, .place_name")
            if name_tag:
                name = name_tag.get_text().strip()
                if name and name not in places:
                    places.append(name)

        # 현재 수집된 리스트 로그 (디버깅용)
        print(f"\n[{keyword}] 상위 리스트: {places[:10]}")

        # 순위 비교 (공백 제거)
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
            
    except Exception as e:
        print(f"오류: {e}")
        return "분석 오류"

if __name__ == "__main__":
    # 서초우물 7위 기준 확인을 위한 실행
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [실시간 순위 보고]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
