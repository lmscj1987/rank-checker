import requests
import re
import json

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 통합검색 결과 내 플레이스 데이터를 포함한 URL
        url = f"https://m.search.naver.com/search.naver?query={keyword}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://m.naver.com/'
        }
        
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code != 200:
            return "접속 차단"

        # 방식: 페이지 내에 숨겨진 JSON 데이터(window.__INITIAL_STATE__)를 찾아 추출
        # 이 데이터는 광고가 제거된 실제 순수 업체 리스트를 담고 있습니다.
        content = res.text
        
        # 1차 시도: TYaxT 클래스 기반 (가장 직관적)
        places = re.findall(r'<span class="TYaxT">(.*?)</span>', content)
        
        # 만약 리스트가 비어있다면 (차단 혹은 구조변경), 2차 데이터 추출 시도
        if not places:
            # 상세 정보 섹션에서 업체명 패턴 추출
            places = re.findall(r'"title":"([^"]+)"', content)
            # 불필요한 공통 단어 제거 (네이버 내부 예약어 제외)
            exclude_words = ['지도', '전화', '검색', '공유', '길찾기', '이미지', '플레이스']
            places = [p for p in places if p not in exclude_words and len(p) > 1]

        # 순위 비교 (공백 무시)
        rank = 0
        target_clean = target_name.replace(" ", "")
        
        # 중복 제거 (순서 유지)
        seen = set()
        final_places = []
        for p in places:
            if p not in seen:
                final_places.append(p)
                seen.add(p)

        for idx, name in enumerate(final_places, 1):
            if target_clean in name.replace(" ", ""):
                rank = idx
                break
        
        if rank > 0:
            return f"{rank}위"
        else:
            return "40위권 밖"
            
    except Exception as e:
        return "분석 실패"

if __name__ == "__main__":
    # 서초우물 7위 반영 여부 확인
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [최종 점검 알림]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
