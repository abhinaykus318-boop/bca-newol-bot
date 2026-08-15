import os
import json
import requests
from bs4 import BeautifulSoup
from hashlib import sha256

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

DB_FILE = "sent_updates.json"

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
        "https://scholarships.gov.in/",
}

BCA_KEYWORDS = [
    "bca_newol",
    "bca newol",
    "bca online",
    "bachelor of computer applications",
    "bcaol",
    "bcs111",
    "bcs12",
    "bcsl13",
    "begla136",
    "bevae181",
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
    "scholarship",
]


def load_database():

    if not os.path.exists(DB_FILE):
        return []

    try:
        with open(DB_FILE, "r") as file:
            return json.load(file)

    except:
        return []


def save_database(database):

    with open(DB_FILE, "w") as file:
        json.dump(database, file, indent=2)


def send_message(text):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text,
            "disable_web_page_preview": False
        },
        timeout=30
    )


def get_page_text(url):

    try:

        response = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

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
