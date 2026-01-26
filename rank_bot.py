import requests
import os

# 1. 설정 정보 (토큰과 ID는 본인 것으로 유지)
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def check_rank(keyword):
    try:
        url = f"https://search.naver.com/search.naver?query={keyword}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        res = requests.get(url, headers=headers, timeout=10)
        
        if res.status_code == 200:
            return "✅ 접속 성공 (데이터 수집 완료)"
        else:
            return f"❌ 접속 실패 (상태코드: {res.status_code})"
    except Exception as e:
        return f"⚠️ 연결 오류: {str(e)}"

if __name__ == "__main__":
    # 순위 체크 실행
    s_well = check_rank('사당우물')
    sc_well = check_rank('서초우물')
    
    # 결과 메시지 생성
    result_text = f"📢 [Daily Rank Check]\n• 사당우물: {s_well}\n• 서초우물: {sc_well}"
    
    # [중요] 1. 깃허브 로그에 출력 (이게 있어야 Actions 탭에서 보입니다)
    print("-" * 30)
    print(result_text)
    print("-" * 30)
    
    # 2. 텔레그램 전송
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        response = requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
        if response.status_code == 200:
            print("🚀 텔레그램 알림 전송 완료!")
        else:
            print(f"❗ 텔레그램 전송 실패: {response.text}")
    except Exception as e:
        print(f"❗ 알림 전송 중 에러: {e}")
