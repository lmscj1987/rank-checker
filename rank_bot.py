import requests
from bs4 import BeautifulSoup

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 통합검색 결과가 아닌 '플레이스' 탭 결과를 바로 호출
        url = f"https://m.search.naver.com/search.naver?query={keyword}&where=m_local"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
        }
        
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # [핵심] 현재 네이버 모바일 플레이스 리스트의 업체명을 담은 클래스들
        # TYaxT: 업체명 본문 / 스크롤 로딩 대비 다양한 선택자 포함
        place_elements = soup.select(".TYaxT, .place_name, .L_0S_, ._3uY7d")
        
        places = []
        for el in place_elements:
            name = el.get_text().strip()
            # 광고 뱃지가 있는 요소는 제외 (부모 요소 확인)
            parent_text = el.find_parent().get_text() if el.find_parent() else ""
            if "광고" in parent_text[:5]: # 앞부분에 '광고'가 붙어 있으면 스킵
                continue
                
            if name and name not in places:
                places.append(name)
        
        # 디버깅용: 수집된 업체가 없으면 에러로 간주하지 않고 0위 처리
        if not places:
            return "데이터 수집 실패"

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
        return f"분석 오류"

if __name__ == "__main__":
    # 서초우물 7위 기준 재검증 실행
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [최종 복구 보고]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
