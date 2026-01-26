import requests
from bs4 import BeautifulSoup

# 텔레그램 설정
TELEGRAM_TOKEN = "8438716732:AAGLb4rhWyx-G2khyvcfio1-4aRRgBCyz1I"
CHAT_ID = "8479493770"

def get_naver_rank(keyword):
    url = f"https://search.naver.com/search.naver?query={keyword}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    
    try:
        res = requests.get(url, headers=headers)
        # 여기에 실제 순위를 찾는 로직이 들어갑니다. 일단 접속 성공 여부만 체크!
        if res.status_code == 200:
            return "순위 데이터 수집 성공"
        return "접속 실패"
    except:
        return "에러 발생"

if __name__ == "__main__":
    msg = f"📢 [GitHub 자동 알림]\n사당우물: {get_naver_rank('사당우물')}\n서초우물: {get_naver_rank('서초우물')}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': msg})
