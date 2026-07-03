import re
import sqlite3

# Read the resume
file = open("sample_resume.txt", "r")
content = file.read()
file.close()

# Extract email
email = re.findall(r'[\w\.-]+@[\w\.-]+', content)

# Extract phone number
phone = re.findall(r'\+?\d[\d\s-]{8,}\d', content)

# Extract name (first line)
name = content.splitlines()[0].strip()

# Extract skills
skill_list = [
    "Python",
    "SQL",
    "Flask",
    "Machine Learning",
    "HTML",
    "CSS",
    "Java",
    "C++"
]

found_skills = []

for skill in skill_list:
    if skill.lower() in content.lower():
        found_skills.append(skill)

# Display extracted information
print("Name:", name)
print("Email:", email)
print("Phone:", phone)
print("Skills:", found_skills)

# Create SQLite database
conn = sqlite3.connect("candidates.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    skills TEXT
)
""")

cursor.execute(
    "INSERT INTO candidates (name, email, phone, skills) VALUES (?, ?, ?, ?)",
    (
        name,
        email[0] if email else "",
        phone[0] if phone else "",
        ", ".join(found_skills)
    )
)

conn.commit()
conn.close()

print("✅ Candidate information saved successfully!")
