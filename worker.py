from workers import WorkerEntrypoint, Response, fetch
from urllib.parse import urlparse
import json


class Default(WorkerEntrypoint):

    async def fetch(self, request):
        url = urlparse(request.url)

        # Browser se Worker URL open karne par
        if url.path == "/":
            return Response(
                "BCA NEWOL AI Assistant is ONLINE ✅",
                headers={"Content-Type": "text/plain"}
            )

        # Telegram webhook
        if url.path == "/telegram" and request.method == "POST":
            try:
                update = await request.json()
                await self.handle_telegram_update(update)
                return Response("OK")
            except Exception as e:
                print("Webhook error:", str(e))
                return Response("OK")

        return Response("Not Found", status=404)

    async def handle_telegram_update(self, update):

        message = update.get("message")

        if not message:
            return

        chat = message.get("chat", {})
        chat_id = chat.get("id")

        text = message.get("text", "").strip()

        if not chat_id:
            return

        # /start
        if text == "/start":
            reply = (
                "🤖 BCA NEWOL AI Assistant\n\n"
                "✅ Bot successfully connected!\n\n"
                "🎓 Programme: BCA_NEWOL\n\n"
                "📚 Semester 1\n"
                "• BCS-111\n"
                "• BCS-112\n"
                "• BCSL-113\n"
                "• BEGLA-136\n"
                "• BEVAE-181\n\n"
                "Commands:\n"
                "/sem1 - Semester 1 courses\n"
                "/help - Help"
            )

        # /sem1
        elif text == "/sem1":
            reply = (
                "📚 BCA_NEWOL — Semester 1\n\n"
                "1️⃣ BCS-111\n"
                "2️⃣ BCS-112\n"
                "3️⃣ BCSL-113\n"
                "4️⃣ BEGLA-136\n"
                "5️⃣ BEVAE-181"
            )

        # /help
        elif text == "/help":
            reply = (
                "🤖 BCA NEWOL BOT — Help\n\n"
                "/start — Start bot\n"
                "/sem1 — Semester 1 courses\n"
                "/help — Show help"
            )

        else:
            reply = (
                "🤖 BCA NEWOL BOT\n\n"
                "Command samajh nahi aaya.\n\n"
                "/start\n"
                "/sem1\n"
                "/help"
            )

        await self.send_message(chat_id, reply)

    async def send_message(self, chat_id, text):

        token = self.env.TELEGRAM_TOKEN

        api_url = f"https://api.telegram.org/bot{token}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text
        }

        await fetch(
            api_url,
            {
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps(payload)
            }
        )
