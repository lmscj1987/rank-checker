import requests

# 설정 정보
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def check_rank(keyword):
    try:
        url = f"https://search.naver.com/search.naver?query={keyword}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
        res = requests.get(url, headers=headers, timeout=10)
        return "접속 성공" if res.status_code == 200 else "접속 실패"
    except:
        return "연결 오류"

if __name__ == "__main__":
    result_text = f"📢 [자동 알림]\n사당우물: {check_rank('사당우물')}\n서초우물: {check_rank('서초우물')}"
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(send_url, data={'chat_id': CHAT_ID, 'text': result_text})
