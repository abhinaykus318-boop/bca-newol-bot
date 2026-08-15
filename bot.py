import os
import json
import requests
from bs4 import BeautifulSoup
from hashlib import sha256

from course_data import COURSES, format_semester


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

DB_FILE = "sent_updates.json"


# ============================================================
# TELEGRAM
# ============================================================

def telegram_request(method, data=None):

    url = f"https://api.telegram.org/bot{TOKEN}/{method}"

    response = requests.post(
        url,
        json=data or {},
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def send_message(chat_id, text):

    telegram_request(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": False
        }
    )


# ============================================================
# COMMANDS
# ============================================================

def handle_command(chat_id, command):

    command = command.lower().split("@")[0]

    if command == "/start":

        send_message(
            chat_id,
            """🤖 BCA_NEWOL ASSISTANT

Namaste! 👋

🎓 Programme: BCA_NEWOL

📚 Commands:

/sem1 — Semester 1
/sem2 — Semester 2
/sem3 — Semester 3
/sem4 — Semester 4
/sem5 — Semester 5
/sem6 — Semester 6

📋 /courses — All semesters
🗺 /roadmap — BCA roadmap

🎯 Main tumhe BCA_NEWOL ke important
updates aur activities track karne mein help karunga."""
        )

        return


    if command.startswith("/sem"):

        number = command.replace(
            "/sem",
            ""
        )

        if number.isdigit():

            semester = int(number)

            if 1 <= semester <= 6:

                send_message(
                    chat_id,
                    format_semester(
                        semester
                    )
                )

                return


        send_message(
            chat_id,
            "❌ Valid command use karo:\n\n"
            "/sem1\n"
            "/sem2\n"
            "/sem3\n"
            "/sem4\n"
            "/sem5\n"
            "/sem6"
        )

        return


    if command == "/courses":

        message = "🎓 BCA_NEWOL — ALL SEMESTERS\n\n"

        for semester, data in COURSES.items():

            message += (
                f"📚 Semester {semester} "
                f"({data['credits']} Credits)\n"
            )

            for code, name in data[
                "subjects"
            ].items():

                message += (
                    f"• {code} — {name}\n"
                )

            message += "\n"

        send_message(
            chat_id,
            message
        )

        return


    if command == "/roadmap":

        send_message(
            chat_id,
            """🗺 BCA_NEWOL ROADMAP

1️⃣ Semester 1
2️⃣ Semester 2
3️⃣ Semester 3
4️⃣ Semester 4
5️⃣ Semester 5
6️⃣ Semester 6

🎯 Har semester mein:

📚 Study Material
📝 Assignments
🧪 Practical/Lab
📝 TEE
📅 Important deadlines
📢 IGNOU notices

🎓 Semester 5:
BCSP-165 Project Proposal

🎓 Semester 6:
BCSP-165 Project Report + Viva

👉 Abhi apne current semester ke
assignments aur LMS activities check karo."""
        )

        return


    send_message(
        chat_id,
        """❓ Command samajh nahi aaya.

Try:

/start
/sem1
/sem2
/sem3
/sem4
/sem5
/sem6
/courses
/roadmap"""
    )


# ============================================================
# TELEGRAM UPDATES
# ============================================================

def check_telegram_commands():

    try:

        data = telegram_request(
            "getUpdates"
        )

        updates = data.get(
            "result",
            []
        )

        for update in updates:

            message = update.get(
                "message",
                {}
            )

            chat = message.get(
                "chat",
                {}
            )

            chat_id = chat.get(
                "id"
            )

            text = message.get(
                "text",
                ""
            ).strip()

            if chat_id and text.startswith("/"):

                handle_command(
                    chat_id,
                    text.split()[0]
                )

        return updates

    except Exception as error:

        print(
            "Telegram error:",
            error
        )

        return []


# ============================================================
# DATABASE
# ============================================================

def load_database():

    if not os.path.exists(DB_FILE):
        return []

    try:

        with open(
            DB_FILE,
            "r"
        ) as file:

            return json.load(file)

    except:

        return []


def save_database(database):

    with open(
        DB_FILE,
        "w"
    ) as file:

        json.dump(
            database,
            file,
            indent=2
        )


# ============================================================
# WEBSITE SOURCES
# ============================================================

SOURCES = {

    "IGNOU BCA_NEWOL":
        "https://www.ignou.ac.in/schools/programme/BCA_NEWOL",

    "IGNOU Main":
        "https://www.ignou.ac.in/",

    "BCA_NEWOL LMS":
        "https://iop.ignouonline.ac.in/",

    "eGyanKosh":
        "https://egyankosh.ac.in/",

    "Samarth":
        "https://ignou.samarth.edu.in/",

    "RC Varanasi":
        "http://rcvaranasi.ignou.ac.in/",

    "NSP":
        "https://scholarships.gov.in/"
}


BCA_KEYWORDS = [

    "bca_newol",
    "bca newol",
    "bca online",
    "bachelor of computer applications",

    "bcs-111",
    "bcs111",
    "bcs-012",
    "bcs12",
    "bcsl-013",
    "bcsl13",
    "begla-136",
    "begla136",
    "bevae-181",
    "bevae181",

    "feg-02",
    "mcs-202",
    "mcs-203",
    "mcsl-204",
    "mcs-201",
    "mcsl-205",

    "mcs-208",
    "mcsl-209",
    "mcs-207",
    "bcs-131",
    "bcsl-135",
    "bcs-040",

    "mcs-206",
    "bcsl-146",
    "bcs-053",
    "bcsl-147",
    "bcs-041",
    "bcoc-131",

    "bcs-151",
    "bcs-042",
    "bcsl-159",
    "bcos-184",
    "msei-023",
    "becs-184",

    "bcos-185",
    "msei-027",
    "bcsp-165"
]


ACTIVITY_KEYWORDS = [

    "assignment",
    "exam",
    "examination",
    "term end",
    "tee",
    "hall ticket",
    "result",
    "grade card",
    "re-registration",
    "registration",
    "counselling",
    "counseling",
    "practical",
    "workshop",
    "induction",
    "study material",
    "notification",
    "notice",
    "deadline",
    "last date",
    "schedule",
    "date sheet",
    "scholarship"
]


# ============================================================
# WEBSITE READER
# ============================================================

def get_page_text(url):

    try:

        response = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent":
                "Mozilla/5.0 BCA-NEWOL-Tracker"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup([
            "script",
            "style",
            "noscript"
        ]):

            tag.decompose()

        return soup.get_text(
            " ",
            strip=True
        )

    except Exception as error:

        print(
            f"Website error: {error}"
        )

        return ""


# ============================================================
# FILTER
# ============================================================

def is_bca_related(text):

    text = text.lower()

    return any(
        keyword in text
        for keyword in BCA_KEYWORDS
    )


def has_activity(text):

    text = text.lower()

    return any(
        keyword in text
        for keyword in ACTIVITY_KEYWORDS
    )


# ============================================================
# DUPLICATE ID
# ============================================================

def create_id(
    source,
    text
):

    return sha256(
        (
            source +
            text
        ).encode("utf-8")
    ).hexdigest()


# ============================================================
# UPDATE MESSAGE
# ============================================================

def create_message(
    source,
    url,
    text
):

    text = " ".join(
        text.split()
    )

    if len(text) > 1200:

        text = text[:1200] + "..."

    return f"""🚨 BCA_NEWOL UPDATE

🎓 Programme:
BCA_NEWOL

📌 Source:
{source}

📝 Kya update mila:

{text}

🎯 AB MUJHE KYA KARNA CHAHIYE?

1️⃣ Official source open karo.
2️⃣ Apne semester/course ko check karo.
3️⃣ Agar update tumhare liye applicable hai,
to deadline/activity note karo.

⚠️ Exact information official notice se verify karo.

🔗 Official Source:
{url}
"""


# ============================================================
# WEBSITE TRACKER
# ============================================================

def check_websites():

    database = load_database()

    new_updates = 0

    for source, url in SOURCES.items():

        print(
            f"Checking: {source}"
        )

        text = get_page_text(
            url
        )

        if not text:
            continue

        if not is_bca_related(text):
            continue

        if not has_activity(text):
            continue

        update_id = create_id(
            source,
            text
        )

        if update_id in database:

            print(
                "Already sent."
            )

            continue

        message = create_message(
            source,
            url,
            text
        )

        send_message(
            CHAT_ID,
            message
        )

        database.append(
            update_id
        )

        new_updates += 1

    save_database(
        database
    )

    print(
        "New updates:",
        new_updates
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "Starting BCA_NEWOL bot..."
    )

    # Telegram commands
    check_telegram_commands()

    # Website tracker
    check_websites()


if __name__ == "__main__":

    main()            return True

    return False


def has_activity(text):

    text = text.lower()

    for keyword in ACTIVITY_KEYWORDS:

        if keyword in text:
            return True

    return False


def create_id(source, text):

    data = source + text

    return sha256(
        data.encode("utf-8")
    ).hexdigest()


def create_message(
    source,
    url,
    text
):

    text = " ".join(
        text.split()
    )

    if len(text) > 1200:
        text = text[:1200] + "..."

    return f"""
🚨 BCA_NEWOL UPDATE

🎓 Programme:
BCA_NEWOL

📌 Source:
{source}

📝 Kya update mila:

{text}

🎯 AB MUJHE KYA KARNA CHAHIYE?

1️⃣ Official source open karo.
2️⃣ Apne semester/course ko check karo.
3️⃣ Agar applicable hai to date/activity note karo.

⚠️ Exact deadline official notice se verify karo.

🔗 Official Source:
{url}
"""


def main():

    database = load_database()

    new_updates = 0

    for source, url in SOURCES.items():

        print(
            f"Checking {source}"
        )

        text = get_page_text(url)

        if not text:
            continue

        if not is_bca_related(text):
            continue

        if not has_activity(text):
            continue

        update_id = create_id(
            source,
            text
        )

        if update_id in database:

            print(
                "Already sent - skipping"
            )

            continue

        message = create_message(
            source,
            url,
            text
        )

        send_message(message)

        database.append(
            update_id
        )

        new_updates += 1

    save_database(database)

    print(
        f"New updates: {new_updates}"
    )


if __name__ == "__main__":
    main()        for tag in soup([
            "script",
            "style",
            "noscript"
        ]):
            tag.decompose()

        return soup.get_text(
            " ",
            strip=True
        )

    except Exception as error:

        print(
            f"Error reading {url}: {error}"
        )

        return ""


def is_bca_related(text):

    text = text.lower()

    for keyword in BCA_KEYWORDS:

        if keyword in text:
            return True

    return False


def has_activity(text):

    text = text.lower()

    for keyword in ACTIVITY_KEYWORDS:

        if keyword in text:
            return True

    return False


def create_id(source, text):

    data = source + text

    return sha256(
        data.encode("utf-8")
    ).hexdigest()


def create_message(
    source,
    url,
    text
):

    text = " ".join(
        text.split()
    )

    if len(text) > 1200:
        text = text[:1200] + "..."

    return f"""
🚨 BCA_NEWOL UPDATE

🎓 Programme:
BCA_NEWOL

📌 Source:
{source}

📝 Kya update mila:

{text}

🎯 AB MUJHE KYA KARNA CHAHIYE?

1️⃣ Official source open karo.
2️⃣ Apne semester/course ko check karo.
3️⃣ Agar applicable hai to date/activity note karo.

⚠️ Exact deadline official notice se verify karo.

🔗 Official Source:
{url}
"""


def main():

    database = load_database()

    new_updates = 0

    for source, url in SOURCES.items():

        print(
            f"Checking {source}"
        )

        text = get_page_text(url)

        if not text:
            continue

        if not is_bca_related(text):
            continue

        if not has_activity(text):
            continue

        update_id = create_id(
            source,
            text
        )

        if update_id in database:

            print(
                "Already sent - skipping"
            )

            continue

        message = create_message(
            source,
            url,
            text
        )

        send_message(message)

        database.append(
            update_id
        )

        new_updates += 1

    save_database(database)

    print(
        f"New updates: {new_updates}"
    )


if __name__ == "__main__":
    main()
