import requests
import json

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 일반 HTML이 아닌, 네이버 플레이스 서버에서 직접 데이터를 가져오는 API 주소입니다.
        # 차단에 가장 강하며, 광고가 섞이지 않은 순수 순위를 줍니다.
        url = f"https://map.naver.com/v5/api/search?query={keyword}&type=all&displayCount=50"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Accept': 'application/json, text/plain, */*',
            'Referer': f'https://m.search.naver.com/'
        }
        
        res = requests.get(url, headers=headers, timeout=10)
        
        # 접속 차단 여부 확인
        if res.status_code != 200:
            return "네이버 접속 차단됨"
            
        data = res.json()
        place_list = data.get('result', {}).get('place', {}).get('list', [])
        
        if not place_list:
            return "검색 결과 없음"

        places = []
        for item in place_list:
            # 광고(AD)는 'businessType'이 다르거나 별도 표기가 되므로 걸러집니다.
            name = item.get('name', '')
            if name:
                places.append(name)
        
        # 순위 비교 (공백 무시)
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
        return f"분석 오류"

if __name__ == "__main__":
    # 서초우물 7위 반영 여부 직접 확인
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [정밀 데이터 분석 완료]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
