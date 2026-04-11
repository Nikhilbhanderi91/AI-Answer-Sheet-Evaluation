import re
import csv
import os

# =========================
# CREATE RESULTS FOLDER
# =========================
os.makedirs("results", exist_ok=True)

# =========================
# READ OCR TEXT FILES
# =========================
model_file_path = "processed/model/text/model.txt"
student_file_path = "processed/students/student_1/text/student.txt"

# safety check
if not os.path.exists(model_file_path):
    print("❌ Model OCR file not found")
    exit()

if not os.path.exists(student_file_path):
    print("❌ Student OCR file not found")
    exit()

with open(model_file_path, "r", encoding="utf-8") as f:
    model_text = f.read()

with open(student_file_path, "r", encoding="utf-8") as f:
    student_text = f.read()

print("✅ OCR text files loaded")


# =========================
# FIX OCR LETTER ERRORS
# =========================
def normalize_answer(ans):
    ans = ans.upper().strip()

    # Common OCR mistakes
    replacements = {
        "8": "B",
        "0": "D",
        "O": "D",
        "Q": "B",
        "P": "D",
        "£": "B",
        "]": "B",
        "[": "C",
        "{": "C",
        "}": "C",
        "(": "C",
        ")": "C",
        "I": "B",
        "L": "B",
        "S": "B",
        "|": "I"
    }

    for wrong, correct in replacements.items():
        ans = ans.replace(wrong, correct)

    # extract only valid answer A/B/C/D
    match = re.search(r'[A-D]', ans)
    return match.group() if match else ""


# =========================
# EXTRACT ANSWERS
# =========================
def extract_answers(text):
    """
    Extract only Answer: values
    """
    pattern = r'Answer[:\s]*([A-Za-z0-9£{}\]\[\(\)\|]+)'
    raw_answers = re.findall(pattern, text, flags=re.IGNORECASE)

    cleaned_answers = []

    for ans in raw_answers:
        fixed = normalize_answer(ans)

        if fixed in ["A", "B", "C", "D"]:
            cleaned_answers.append(fixed)

    return cleaned_answers


# =========================
# GET ANSWERS
# =========================
model_answers = extract_answers(model_text)
student_answers = extract_answers(student_text)

print("\n📘 MODEL ANSWERS :", model_answers)
print("🧑 STUDENT ANSWERS:", student_answers)


# =========================
# AUTO DETECT TOTAL QUESTIONS
# =========================
total = len(model_answers)

# If OCR misses some student answers,
# fill blanks for missing questions
while len(student_answers) < total:
    student_answers.append("")

# Remove extra noise answers
student_answers = student_answers[:total]

# =========================
# COMPARE ANSWERS
# =========================
score = 0

for i in range(total):
    if model_answers[i] == student_answers[i]:
        score += 1

percentage = (score / total) * 100 if total > 0 else 0

# =========================
# DISPLAY RESULT
# =========================
print("\n📊 FINAL RESULT")
print("Marks      :", score)
print("Total      :", total)
print("Percentage :", round(percentage, 2), "%")


# =========================
# SAVE CSV (FRESH WRITE)
# =========================
file_path = "results/results.csv"

with open(file_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "Student_ID",
        "Marks",
        "Total",
        "Percentage"
    ])

    writer.writerow([
        "student_1",
        score,
        total,
        round(percentage, 2)
    ])

print("✅ Result saved successfully in results/results.csv")