import os
import requests
from bs4 import BeautifulSoup

# [보안 적용] GitHub Secrets에 저장한 값을 불러옵니다.
token = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')

def send_telegram_message(message):
    """텔레그램으로 메시지를 전송합니다."""
    if not token or not chat_id:
        print("에러: TELEGRAM_TOKEN 또는 CHAT_ID가 설정되지 않았습니다.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("메시지 전송 성공!")
        else:
            print(f"메시지 전송 실패: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"오류 발생: {e}")

def main():
    # 여기에 어제 만든 크롤링 로직을 넣으시면 됩니다.
    # 예시:
    target_url = "https://example.com" # 순위 확인할 사이트 주소
    print(f"{target_url}에서 순위 확인 중...")
    
    # 임시 결과 메시지 (실제 로직으로 대체하세요)
    result_text = "오늘의 순위 확인 결과가 정상적으로 생성되었습니다!"
    
    # 텔레그램 전송
    send_telegram_message(result_text)

if __name__ == "__main__":
    main()
