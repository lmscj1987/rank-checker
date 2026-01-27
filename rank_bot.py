import requests
import re

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 플레이스 검색 결과 데이터 호출
        url = f"https://m.search.naver.com/p/api/search.naver?where=m_local&query={keyword}&display=100"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://m.naver.com/'
        }
        
        res = requests.get(url, headers=headers, timeout=10)
        content = res.text

        # [핵심] 광고 영역과 일반 영역 분리
        # 네이버 API 응답에서 광고(ad) 섹션을 버리고 실제 리스트(ls) 섹션만 추출합니다.
        # 이렇게 해야 광고 4개를 건너뛰고 '서초우물 7위'가 정확히 나옵니다.
        
        real_list_part = re.split(r'\"ls\":', content)
        if len(real_list_part) < 2:
            return "데이터 구조 분석 불가"
            
        # 실제 순위 업체들만 추출
        found_titles = re.findall(r'\"title\":\"([^"]+)\"', real_list_part[1])
        
        places = []
        exclude = ['지도', '전화', '검색', '공유', '길찾기', '이미지', '플레이스', '네이버', '더보기']
        
        for t in found_titles:
            if t not in exclude and len(t) > 1:
                if t not in places:
                    places.append(t)

        # 내 업체 순위 매칭
        rank = 0
        target_clean = target_name.replace(" ", "")
        for idx, name in enumerate(places, 1):
            if target_clean in name.replace(" ", ""):
                rank = idx
                break
        
        if rank > 0:
            return f"{rank}위"
        else:
            return "100위권 밖"
            
    except Exception:
        return "분석 오류"

if __name__ == "__main__":
    # 요청하신 검색 키워드 및 타겟 업체 설정
    # 1. '사당술집' 검색 시 '사당우물'
    res1 = get_naver_rank('사당술집', '사당우물')
    
    # 2. '교대술집' 검색 시 '서초우물' (기준: 7위)
    res2 = get_naver_rank('교대술집', '서초우물')
    
    result_text = f"📊 [정밀 순위 리포트]\n\n🍺 사당술집 내 '사당우물': {res1}\n🍺 교대술집 내 '서초우물': {res2}"
    
    # 결과 출력 및 텔레그램 전송
    print(result_text)
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
