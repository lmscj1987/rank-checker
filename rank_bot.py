import requests
import re

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 네이버 플레이스 데이터를 직접 가져오는 API 주소
        url = f"https://m.search.naver.com/p/api/search.naver?where=m_local&query={keyword}&display=100&start=1"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://m.search.naver.com/'
        }
        
        res = requests.get(url, headers=headers, timeout=15)
        content = res.text

        # 1. 광고(AD) 섹션과 일반(LS) 섹션을 구분하여 데이터 추출
        # 광고를 포함하지 않는 실제 순위 리스트(ls)만 타겟팅합니다.
        ls_part = content.split('"ls":[')
        if len(ls_part) < 2:
            return "데이터 수집 실패"

        # 실제 순위 업체들의 제목만 추출
        found_titles = re.findall(r'\"title\":\"([^"]+)\"', ls_part[1])
        
        # 중복 및 노이즈 제거
        places = []
        for t in found_titles:
            if len(t) > 1 and t not in places:
                places.append(t)

        # 2. 내 업체 순위 매칭
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
            
    except Exception as e:
        return "분석 오류"

if __name__ == "__main__":
    # 요청하신 검색 키워드와 업체명
    res1 = get_naver_rank('사당술집', '사당우물')
    res2 = get_naver_rank('교대술집', '서초우물') # 여기서 7위가 나와야 성공입니다.
    
    result_text = f"📊 [정밀 순위 리포트]\n\n🍺 사당술집 ->
