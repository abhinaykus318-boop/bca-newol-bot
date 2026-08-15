import os
import requests
from bs4 import BeautifulSoup
from hashlib import sha256


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


# ============================================================
# YOUR BCA_NEWOL COURSE
# ============================================================

PROGRAMME = "BCA_NEWOL"

SUBJECTS = [
    "BCS111",
    "BCS12",
    "BCSL13",
    "BEGLA136",
    "BEVAE181",
]


# ============================================================
# OFFICIAL / IMPORTANT SOURCES
# ============================================================

SOURCES = {
    "IGNOU BCA_NEWOL":
        "https://www.ignou.ac.in/schools/programme/BCA_NEWOL",

    "IGNOU Assignments":
        "https://www.ignou.ac.in/studentService/download/assignments",

    "IGNOU Main":
        "https://www.ignou.ac.in/",

    "BCA_NEWOL LMS":
        "https://iop.ignouonline.ac.in/programme/p76",

    "BCA_NEWOL Announcements":
        "https://iop.ignouonline.ac.in/announcements/0",

    "eGyanKosh":
        "https://egyankosh.ac.in/",

    "Samarth Student Portal":
        "https://ignou.samarth.edu.in/",

    "RC Varanasi":
        "http://rcvaranasi.ignou.ac.in/",

    "NSP":
        "https://scholarships.gov.in/",
}


# ============================================================
# WORDS WE CARE ABOUT
# ============================================================

BCA_KEYWORDS = [
    "bca_newol",
    "bca newol",
    "bca-online",
    "bca online",
    "bachelor of computer applications",
    "bcaol",
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
    "lms",
    "study material",
    "academic",
    "notification",
    "notice",
    "deadline",
    "last date",
    "schedule",
    "date sheet",
    "scholarship",
    "nsp",
]


# ============================================================
# TELEGRAM
# ============================================================

def send_message(text):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text,
            "disable_web_page_preview": False
        },
        timeout=30
    )

    response.raise_for_status()


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

        # Remove unnecessary elements
        for tag in soup([
            "script",
            "style",
            "noscript"
        ]):
            tag.decompose()

        text = soup.get_text(
            " ",
            strip=True
        )

        return text

    except Exception as error:

        print(
            f"Could not read {url}: {error}"
        )

        return ""


# ============================================================
# BCA FILTER
# ============================================================

def is_bca_related(text):

    text = text.lower()

    # Strong BCA_NEWOL match
    for keyword in BCA_KEYWORDS:

        if keyword in text:

            return True

    # Subject-code match
    subject_matches = 0

    for subject in SUBJECTS:

        if subject.lower() in text:

            subject_matches += 1

    # At least one BCA subject mentioned
    if subject_matches >= 1:

        return True

    return False


# ============================================================
# ACTIVITY FILTER
# ============================================================

def contains_activity(text):

    text = text.lower()

    for keyword in ACTIVITY_KEYWORDS:

        if keyword in text:

            return True

    return False


# ============================================================
# CREATE SIMPLE HINGLISH MESSAGE
# ============================================================

def make_message(
    source_name,
    source_url,
    page_text
):

    # Keep Telegram message short
    cleaned = " ".join(
        page_text.split()
    )

    if len(cleaned) > 1200:

        cleaned = cleaned[:1200] + "..."


    message = f"""
🚨 BCA_NEWOL UPDATE

📚 Programme:
BCA_NEWOL

📌 Source:
{source_name}

📝 Kya mila:
{cleaned}

🎯 AB MUJHE KYA KARNA CHAHIYE?

1️⃣ Official source open karo.
2️⃣ BCA_NEWOL / apne subject ko check karo.
3️⃣ Agar update tumhare semester par apply hota hai, date/activity note karo.

⚠️ Important:
Exact deadline ya instruction ke liye official notice zaroor verify karo.

🔗 Official Source:
{source_url}
"""

    return message


# ============================================================
# DUPLICATE CHECK
# ============================================================

def make_hash(text):

    return sha256(
        text.encode("utf-8")
    ).hexdigest()


# ============================================================
# MAIN
# ============================================================

def main():

    print("Starting BCA_NEWOL tracker...")

    found = 0

    for source_name, source_url in SOURCES.items():

        print(
            f"Checking: {source_name}"
        )

        text = get_page_text(
            source_url
        )

        if not text:

            continue


        # Only BCA related information
        if not is_bca_related(text):

            print(
                "Not BCA_NEWOL related."
            )

            continue


        # Ignore pages that contain
        # no meaningful student activity
        if not contains_activity(text):

            print(
                "No important activity detected."
            )

            continue


        found += 1


        message = make_message(
            source_name,
            source_url,
            text
        )


        print(message)


        # ----------------------------------------------------
        # IMPORTANT
        #
        # For the FIRST real version we send the result.
        # Later we will add a small database/file so the
        # same update is not sent repeatedly.
        # ----------------------------------------------------

        send_message(message)


    if found == 0:

        print(
            "No BCA_NEWOL activity detected."
        )


if __name__ == "__main__":

    main()
