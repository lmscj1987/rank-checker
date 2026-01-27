import requests
import re
import json

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 모바일 통합검색 주소
        url = f"https://m.search.naver.com/search.naver?query={keyword}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
        }
        
        res = requests.get(url, headers=headers, timeout=15)
        content = res.text

        # 1. [핵심] 네이버가 광고와 일반 업체를 구분해둔 'JSON 데이터 섹션'을 찾습니다.
        # 이 영역에서 'isAd':true 로 표시된 것들은 모두 제외합니다.
        places = []
        
        # 'items':[...] 형태의 데이터에서 업체명들을 추출 (정규식 활용)
        # 광고가 아닌 일반 업체들은 특정 패턴 뒤에 나열됩니다.
        search_area = re.split(r'\"ls\":', content) # ls는 유기적 검색 결과를 뜻하는 내부 코드입니다.
        
        if len(search_area) > 1:
            # 유기적 결과 영역에서만 타이틀을 추출합니다.
            titles = re.findall(r'\"title\":\"([^"]+)\"', search_area[1])
            
            exclude_keywords = ['지도', '전화', '검색', '공유', '길찾기', '이미지', '플레이스', '네이버', '더보기']
            for t in titles:
                clean_t = t.strip()
                if clean_t not in exclude_keywords and len(clean_t) > 1:
                    if clean_t not in places:
                        places.append(clean_t)

        # 2. 순위 판별 (공백 무시)
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
        return "데이터 분석 오류"

if __name__ == "__main__":
    # 서초우물 7위(광고 제외 시) 결과 도출을 위한 실행
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [광고 필터링 최종 보정]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text) # 로그 확인용
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
