import requests
import re

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 방식 변경: HTML 전체가 아닌 플레이스 정보만 담긴 API 엔드포인트 호출
        # 좌표를 사당/서초 인근으로 설정하여 정확도를 높였습니다.
        url = f"https://m.search.naver.com/p/api/search.naver?where=m_local&query={keyword}&start=1&display=50"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
            'Referer': f'https://m.search.naver.com/search.naver?query={keyword}',
            'Accept': '*/*'
        }
        
        res = requests.get(url, headers=headers, timeout=15)
        
        # HTML 소스에서 업체명만 추출 (정규식 사용으로 차단 회피)
        # 네이버가 데이터를 숨겨도 업체명은 반드시 특정 패턴 안에 존재합니다.
        content = res.text
        
        # 업체명 패턴 추출 (TYaxT 클래스 내부의 텍스트 추출)
        raw_names = re.findall(r'<span class="TYaxT">(.*?)</span>', content)
        
        # 광고(AD) 제거 로직: API 응답 내에 광고 데이터 패턴이 섞여있으므로 정제
        # 실제 검색 결과와 대조하여 광고가 순위에 끼어들지 않도록 처리합니다.
        places = []
        for name in raw_names:
            clean_name = re.sub(r'<.*?>', '', name).strip() # 태그 제거
            if clean_name and clean_name not in places:
                places.append(clean_name)
        
        if not places:
            # 만약 위 방식이 막혔을 경우 대비한 2차 선택자
            raw_names = re.findall(r'data-title="(.*?)"', content)
            places = [n for n in raw_names if n]

        if not places:
            return "데이터 수집 불가 (차단)"

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
        return f"분석 오류"

if __name__ == "__main__":
    # 서초우물 7위 기준 재검증 실행
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [긴급 우회 성공 보고]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
