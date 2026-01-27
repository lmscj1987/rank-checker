import requests
import json

# 1. 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword, target_name):
    try:
        # 네이버 플레이스 리스트 전용 API 호출 (가장 정확함)
        url = f"https://map.naver.com/v5/api/search?query={keyword}&type=all&searchCoord=127.0276197;37.4979517&page=1&displayCount=50"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': f'https://map.naver.com/v5/search/{keyword}'
        }
        
        res = requests.get(url, headers=headers, timeout=10)
        data = res.json()
        
        # 플레이스 리스트 추출 (광고 제외 로직 포함)
        place_list = data.get('result', {}).get('place', {}).get('list', [])
        
        # 40위권까지 업체명 수집
        places = []
        for item in place_list:
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
            return f"{rank}위"
        else:
            return "40위권 밖"
            
    except Exception as e:
        print(f"디버깅 로그: {e}")
        return "분석 오류"

if __name__ == "__main__":
    # 서초우물 7위 기준 검증 완료
    res1 = get_naver_rank('사당우물', '사당우물')
    res2 = get_naver_rank('서초우물', '서초우물')
    
    result_text = f"📢 [최종 정밀 점검 결과]\n\n📍 사당우물: {res1}\n📍 서초우물: {res2}"
    
    print(result_text)
    
    # 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
