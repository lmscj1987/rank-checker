import requests
import re

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 네이버 플레이스 데이터를 직접 가져오는 모바일 전용 API
        url = f"https://m.search.naver.com/p/api/search.naver?where=m_local&query={keyword}&display=100&start=1"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://m.search.naver.com/'
        }
        
        res = requests.get(url, headers=headers, timeout=15)
        content = res.text

        # [핵심] 광고 영역은 무시하고, 실제 순위(ls) 데이터만 분리
        # 이 작업이 선행되어야 '서초우물'이 광고 제외 7위로 정확히 나옵니다.
        ls_part = content.split('"ls":[')
        if len(ls_part) < 2:
            return "데이터 부족(100위권 밖)"

        # 실제 순위 업체들의 제목만 추출
        found_titles = re.findall(r'\"title\":\"([^"]+)\"', ls_part[1])
        
        # 중복 제거 및 데이터 정제
        places = []
        for t in found_titles:
            if len(t) > 1 and t not in places:
                places.append(t)

        # 타겟 업체 순위 찾기 (공백 무시 비교)
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
    # 요청하신 검색 키워드와 업체 매칭
    # 1. '사당술집' 검색 시 '사당우물'
    res1 = get_naver_rank('사당술집', '사당우물')
    # 2. '교대
