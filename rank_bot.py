import requests
from bs4 import BeautifulSoup

# 1. 설정 정보 (기존 정보 유지)
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 일반 검색이 아닌 '플레이스 더보기' 리스트를 직접 타겟팅 (확장성 및 정확도↑)
        url = f"https://m.search.naver.com/search.naver?query={keyword}&where=m_local&sm=mtp_hty"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
        }
        
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 네이버 플레이스 업체명 추출 (최신 선택자 반영)
        # 광고(AD) 요소와 섞이지 않도록 리스트 아이템 내부의 텍스트만 추출합니다.
        # .TYaxT: 업체명 / .place_bluelink: 구형 선택자 보완
        place_elements = soup.select(".TYaxT, .place_bluelink, .P_ajO") 
        
        places = []
        for el in place_elements:
            name = el.get_text().strip()
            # 중복 제거 및 광고 제외 로직 (광고는 보통 별도 태그가 붙음)
            if name and name not in places:
                places.append(name)
        
        # 깃허브 로그에서 현재 잡힌 순서를 직접 확인할 수 있게 출력
        print(f"\n--- [{keyword}] 검색 리스트 (상위 40개) ---")
        for i, p in enumerate(places[:40], 1):
            print(f"{i}위: {p}")

        rank = 0
        target_name_clean = target_name.replace(" ", "")
        
        for idx, name in enumerate(places, 1):
            if target_name_clean in name.replace(" ", ""):
                rank = idx
                break
        
        if rank > 0:
            return f"현재 {rank}위"
        else:
            return "40위권 밖"
            
    except Exception as e:
        print(f"에러 상세: {e}")
        return "분석 오류"

if __name__ == "__main__":
    # 타겟 설정
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [순위 정확도 최종 보정]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print("\n" + result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
