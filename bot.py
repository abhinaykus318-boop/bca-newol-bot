import os
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

def main():
    send_message(
        """🤖 BCA NEWOL BOT

✅ Bot successfully connected!

🎓 Programme: BCA_NEWOL

🎯 AB MUJHE KYA KARNA CHAHIYE?

👉 Next step mein IGNOU updates
aur BCA course filtering add karenge."""
    )

if __name__ == "__main__":
    main()
