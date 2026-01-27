import requests
import re

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 네이버 플레이스 데이터를 직접 가져오는 주소
        url = f"https://m.search.naver.com/p/api/search.naver?where=m_local&query={keyword}&display=100&start=1"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://m.search.naver.com/'
        }
        
        res = requests.get(url, headers=headers, timeout=15)
        content = res.text

        # 1. 광고(AD) 섹션을 버리고 실제 순위(LS) 섹션만 추출
        # 이렇게 해야 '교대술집' 검색 시 서초우물이 정확히 7위로 잡힙니다.
        ls_part = content.split('"ls":[')
        if len(ls_part) < 2:
            return "100위권 밖"

        # 실제 순위 업체들의 제목만 추출
        found_titles = re.findall(r'\"title\":\"([^"]+)\"', ls_part[1])
        
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
        
        return f"{rank}위" if rank > 0 else "100위권 밖"
            
    except:
        return "분석 실패"

if __name__ == "__main__":
    # 요청하신 검색어와 타겟 업체 매칭
    r1 = get_naver_rank('사당술집', '사당우물')
    r2 = get_naver_rank('교대술집', '서초우물') # 목표: 7위
    
    msg = f"📊 [광고제외 정밀 순위]\n\n🍺 사당술집 -> 사당우물: {r1}\n🍺 교대술집 -> 서초우물: {r2}"
    
    # 텔레그램 전송 (이 코드가 실행되면 무조건 메시지가 가야 합니다)
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': msg})
    print(msg)
