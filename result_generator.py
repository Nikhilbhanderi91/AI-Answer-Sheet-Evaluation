import re
import csv
import os

# =========================
# READ FILES
# =========================
with open("processed/model/text/model.txt", "r") as f:
    model_text = f.read()

with open("processed/students/student_1/text/student.txt", "r") as f:
    student_text = f.read()

print("✅ Files Loaded")

# =========================
# REMOVE HEADER
# =========================
def remove_header(text):
    if "1." in text:
        return text.split("1.", 1)[1]
    return text

model_text = remove_header(model_text)
student_text = remove_header(student_text)

# =========================
# CLEAN TEXT (STEP 2 FIX 🔥)
# =========================
def clean_text(text):
    text = re.sub(r'([A-D])(\d+\.)', r'\1\n\2', text)
    text = re.sub(r'([A-D])Q\.', r'\1\nQ.', text)
    text = re.sub(r'(\d+)\.', r'\1. ', text)
    text = re.sub(r'(?<!\n)(\d+\.)', r'\n\1', text)
    return text

model_text = clean_text(model_text)
student_text = clean_text(student_text)

# =========================
# SPLIT MCQs
# =========================
def split_mcqs(text):
    questions = re.split(r'\n(?=\d+\.)', text)
    return [q.strip() for q in questions if q.strip()]

model_mcqs = split_mcqs(model_text)
student_mcqs = split_mcqs(student_text)

print("Model:", len(model_mcqs))
print("Student:", len(student_mcqs))

# =========================
# EXTRACT OPTION (STEP 3 FINAL 🔥)
# =========================
def extract_option(text):
    text = text.upper()
    
    # 🔥 Fix OCR mistakes (advanced)
    replacements = {
        "8": "B",
        "0": "D",
        "O": "D",
        "Q": "B",
        "P": "D",
        "|": "I"
    }
    
    for k, v in replacements.items():
        text = text.replace(k, v)
    
    # 🔥 PRIORITY: Answer: X
    match = re.search(r'ANSWER[:\s]*([A-D])', text)
    if match:
        return match.group(1)
    
    # 🔥 SECOND: detect last valid option
    options = re.findall(r'\b([A-D])\b', text)
    if options:
        return options[-1]
    
    return ""

# =========================
# DEBUG (VERY IMPORTANT 🔥)
# =========================
print("\n--- DEBUG ---")
for i in range(min(len(model_mcqs), len(student_mcqs))):
    m = extract_option(model_mcqs[i])
    s = extract_option(student_mcqs[i])
    print(f"Q{i+1}: Model={m}, Student={s}")

# =========================
# COMPARE
# =========================
score = 0
total = min(len(model_mcqs), len(student_mcqs))

for i in range(total):
    m = extract_option(model_mcqs[i])
    s = extract_option(student_mcqs[i])
    
    if m == s and m != "":
        score += 1

percentage = (score / total) * 100

print("\n📊 FINAL RESULT")
print("Score:", score)
print("Total:", total)
print("Percentage:", round(percentage, 2), "%")

# =========================
# SAVE RESULT
# =========================
file_path = "results/results.csv"

file_exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0

with open(file_path, "a", newline="") as f:
    writer = csv.writer(f)
    
    if not file_exists:
        writer.writerow(["Student_ID", "Marks", "Total", "Percentage"])
    
    writer.writerow(["student_1", score, total, round(percentage, 2)])

print("✅ Result Saved")