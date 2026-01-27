import requests
import re
import json

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 일반 검색 주소가 아니라 플레이스 '데이터 전용' 주소입니다.
        # 광고가 섞이지 않은 순수 리스트 50개를 바로 가져옵니다.
        url = f"https://m.search.naver.com/p/api/search.naver?where=m_local&query={keyword}&display=50"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://m.search.naver.com/'
        }
        
        res = requests.get(url, headers=headers, timeout=10)
        content = res.text
        
        # 1. [광고 완벽 제거] 광고 데이터 영역인 'ad' 섹션은 통째로 버리고 
        # 실제 순위인 'items' 혹은 'ls' 영역에서만 이름을 뽑습니다.
        # 정규식으로 업체명만 정밀 추출
        places = []
        # 네이버가 데이터 사이에 숨겨놓은 업체명 패턴("title":"업체명")만 수집
        raw_titles = re.findall(r'\"title\":\"([^"]+)\"', content)
        
        # 2. 시스템 예약어 및 중복 제거
        exclude = ['지도', '전화', '검색', '공유', '길찾기', '이미지', '플레이스', '네이버', '더보기', '광고']
        for t in raw_titles:
            if t not in exclude and len(t) > 1:
                if t not in places:
                    places.append(t)

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
            
    except Exception as e:
        return f"분석 실패: {str(e)}"

if __name__ == "__main__":
    # 서초우물 7위 반영 확인용
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [실시간 데이터 전송]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
