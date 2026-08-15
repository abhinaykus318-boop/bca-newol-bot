COURSES = {

    1: {
        "name": "Semester 1",
        "credits": 20,
        "subjects": {
            "BEVAE-181": "Environmental Studies",
            "BEGLA-136": "English at Workplace",
            "BCS-111": "Computer Basics and PC Software",
            "BCSL-013": "Computer Basics and PC Software Lab",
            "BCS-012": "Basic Mathematics"
        }
    },

    2: {
        "name": "Semester 2",
        "credits": 20,
        "subjects": {
            "FEG-02": "Foundation Course in English-2",
            "MCS-202": "Computer Organisation",
            "MCS-203": "Operating Systems",
            "MCSL-204": "Windows and Linux Lab",
            "MCS-201": "Programming in C and Python",
            "MCSL-205": "C and Python Lab"
        }
    },

    3: {
        "name": "Semester 3",
        "credits": 20,
        "subjects": {
            "MCS-208": "Data Structures and Algorithms",
            "MCSL-209": "Data Structures and Algorithms Lab",
            "MCS-207": "Database Management Systems",
            "BCS-131": "Programming in C++",
            "BCSL-135": "DBMS and C++ Lab",
            "BCS-040": "Statistical Techniques"
        }
    },

    4: {
        "name": "Semester 4",
        "credits": 20,
        "subjects": {
            "MCS-206": "Object Oriented Programming using Java",
            "BCSL-146": "Object Oriented Programming using Java Lab",
            "BCS-053": "Web Programming",
            "BCSL-147": "Web Programming Lab",
            "BCS-041": "Fundamentals of Computer Networks",
            "BCOC-131": "Financial Accounting"
        }
    },

    5: {
        "name": "Semester 5",
        "credits": 20,
        "subjects": {
            "BCS-151": "Introduction to Software Engineering",
            "BCS-042": "Introduction to Algorithm Design",
            "BCSL-159": "Introduction to Algorithm Design Lab",
            "BCOS-184": "E-Commerce",
            "MSEI-023": "Cyber Security",
            "BECS-184": "Data Analysis"
        }
    },

    6: {
        "name": "Semester 6",
        "credits": 20,
        "subjects": {
            "BCOS-185": "Entrepreneurship",
            "MSEI-027": "Digital Forensics",
            "BCSP-165": "Project"
        }
    }
}


def get_semester(semester):

    return COURSES.get(semester)


def format_semester(semester):

    data = get_semester(semester)

    if not data:
        return "❌ Semester 1 se 6 ke beech number choose karo."

    message = f"🎓 BCA_NEWOL\n\n"
    message += f"📚 {data['name']}\n"
    message += f"💳 Total Credits: {data['credits']}\n\n"

    for code, name in data["subjects"].items():
        message += f"🔹 {code} — {name}\n"

    message += "\n🎯 AB MUJHE KYA KARNA CHAHIYE?\n"
    message += "👉 Apne semester ke subjects check karo.\n"
    message += "👉 LMS par assignments/study material check karo.\n"
    message += "👉 Important IGNOU notices aur deadlines miss mat karo."

    return message
