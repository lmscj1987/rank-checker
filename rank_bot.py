import requests
import re
import json

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 1. 모바일 통합 검색 주소 (가장 데이터가 풍부함)
        url = f"https://m.search.naver.com/search.naver?query={keyword}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://m.naver.com/'
        }
        
        res = requests.get(url, headers=headers, timeout=15)
        content = res.text

        # 2. [핵심] 페이지 내에 숨겨진 업체명 리스트를 정규식으로 직접 추출
        # 'title':'업체명' 패턴을 찾아냅니다. (광고는 보통 이 패턴에서 제외됨)
        raw_titles = re.findall(r'"title":"([^"]+)"', content)
        
        # 3. 데이터 정제 (불필요한 키워드 제외)
        exclude_words = ['지도', '전화', '검색', '공유', '길찾기', '이미지', '플레이스', '네이버', '더보기']
        places = []
        for t in raw_titles:
            # 한글/영문/숫자만 남기고 정제
            clean_t = re.sub(r'\\u[0-9a-fA-F]{4}', '', t).strip()
            if clean_t and clean_t not in exclude_words and len(clean_t) > 1:
                if clean_t not in places:
                    places.append(clean_t)

        # 디버깅 로그 (로그를 보면 현재 네이버가 무엇을 보내주는지 알 수 있음)
        print(f"[{keyword}] 수집된 업체 리스트: {places[:10]}")

        # 4. 순위 비교 (공백 무시)
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
        return f"분석 오류: {str(e)}"

if __name__ == "__main__":
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [도돌이표 탈출 점검]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
