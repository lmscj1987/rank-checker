import requests
import re
import json

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 네이버가 차단을 덜 하는 일반 모바일 검색 URL
        url = f"https://m.search.naver.com/search.naver?query={keyword}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://m.naver.com/'
        }
        
        res = requests.get(url, headers=headers, timeout=10)
        content = res.text

        # [핵심 로직] HTML 태그가 아니라 네이버가 내부에 숨겨둔 JSON 변수를 직접 추출
        # 광고(AD) 섹션과 일반 검색(LS) 섹션이 분리된 원천 데이터를 타겟팅합니다.
        places = []
        
        # 'ls' (유기적 검색 결과) 섹션에서 타이틀만 정밀 추출
        # 이 영역은 광고가 포함되지 않은 순수 순위입니다.
        search_data = re.search(r'\"ls\":\[(.*?)\]', content)
        if search_data:
            found_titles = re.findall(r'\"title\":\"([^"]+)\"', search_data.group(1))
            places = [t for t in found_titles if len(t) > 1]
        
        # 만약 위 방식으로 실패 시, 2차 백업 (title 패턴 전체 수집 후 중복 제거)
        if not places:
            all_titles = re.findall(r'\"title\":\"([^"]+)\"', content)
            exclude = ['지도', '전화', '검색', '공유', '길찾기', '이미지', '플레이스', '더보기', '광고']
            for t in all_titles:
                if t not in exclude and t not in places:
                    places.append(t)

        # 순위 비교 (공백 무시)
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
        return "분석 실패"

if __name__ == "__main__":
    # 서초우물 7위 반영 확인
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [최후의 데이터 추출 결과]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
