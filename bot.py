from workers import WorkerEntrypoint, Response
import json

from course_data import format_semester


class Default(WorkerEntrypoint):

    async def fetch(self, request):

        # Telegram webhook request
        if request.method == "POST":
            try:
                update = await request.json()
            except Exception:
                return Response("Invalid JSON", status=400)

            message = update.get("message", {})
            chat = message.get("chat", {})
            text = message.get("text", "")

            chat_id = chat.get("id")

            if not chat_id:
                return Response("OK")

            # /start
            if text == "/start":

                keyboard = {
                    "keyboard": [
                        [{"text": "📚 Semester 1"}, {"text": "📚 Semester 2"}],
                        [{"text": "📚 Semester 3"}, {"text": "📚 Semester 4"}],
                        [{"text": "📚 Semester 5"}, {"text": "📚 Semester 6"}]
                    ],
                    "resize_keyboard": True
                }

                welcome = (
                    "🎓 *Welcome to IGNOU BCA_NEWOL Bot!*\n\n"
                    "📚 Apna semester select karo:\n\n"
                    "1️⃣ Semester 1\n"
                    "2️⃣ Semester 2\n"
                    "3️⃣ Semester 3\n"
                    "4️⃣ Semester 4\n"
                    "5️⃣ Semester 5\n"
                    "6️⃣ Semester 6"
                )

                await self.send_message(
                    chat_id,
                    welcome,
                    keyboard
                )

                return Response("OK")

            # Semester buttons
            if text.startswith("📚 Semester"):

                try:
                    semester = int(text.split()[-1])
                    reply = format_semester(semester)

                    await self.send_message(
                        chat_id,
                        reply
                    )

                except Exception as e:
                    return Response(
                        "Error: " + str(e),
                        status=500
                    )

                return Response("OK")

            # Normal text
            await self.send_message(
                chat_id,
                "👋 Namaste!\n\n"
                "📚 Semester dekhne ke liye /start dabao."
            )

            return Response("OK")

        # Browser se Worker URL open karne par
        return Response(
            "🤖 IGNOU BCA_NEWOL Telegram Bot is running!"
        )


    async def send_message(
        self,
        chat_id,
        text,
        keyboard=None
    ):

        token = self.env.TELEGRAM_TOKEN

        url = (
            "https://api.telegram.org/bot"
            + token
            + "/sendMessage"
        )

        data = {
            "chat_id": chat_id,
            "text": text
        }

        if keyboard:
            data["reply_markup"] = keyboard

        response = await fetch(
            url,
            method="POST",
            headers={
                "Content-Type": "application/json"
            },
            body=json.dumps(data)
        )

        return response
