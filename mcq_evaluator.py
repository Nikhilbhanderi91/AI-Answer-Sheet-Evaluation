import re
import csv
import os
import sys

if len(sys.argv) > 1:
    student_name = sys.argv[1]
else:
    student_name = "student_1"

model_path = "processed/model/text/model.txt"
student_path = f"processed/students/{student_name}/text/student.txt"

try:
    with open(model_path, "r") as f:
        model_text = f.read()

    with open(student_path, "r") as f:
        student_text = f.read()

except FileNotFoundError:
    print("Error: File not found. Check paths.")
    exit()

print("Files Loaded")

print("\n================ MODEL TEXT =================\n")
print(model_text[:500])

print("\n================ STUDENT TEXT =================\n")
print(student_text[:500])

def clean_text(text):
    text = text.upper()

    replacements = {
        "8B": "B",
        "8": "B",
        "BO": "B",
        "B0": "B",
        "AL": "A",
        "A1": "A",
        "O": "D",
        "0": "D",
        "|": "",
        "I": ""
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text

def format_questions(text):
    text = re.sub(r'(\d+\.)', r'\n\1', text)
    return text

def extract_model_answers(text):
    text = text.upper()
    answers = []
    questions = re.split(r'\n\d+\.', text)

    for q in questions:
        match = re.search(r'ANSWER[:\s]*([A-D])', q)
        if match:
            answers.append(match.group(1))

    return answers

def extract_student_answers(text):
    text = clean_text(text)
    answers = []

    questions = re.split(r'(?=\b\d+\.)', text)

    for q in questions:
        match = re.search(r'ANSWER[:\s]*([A-D])\b', q)

        if match:
            answers.append(match.group(1))
        else:
            options = re.findall(r'\b([A-D])\)', q)

            if len(options) == 1:
                answers.append(options[0])
            elif len(options) > 1:
                answers.append(options[-1])

    return answers

model_text = format_questions(model_text)
model_answers = extract_model_answers(model_text)
student_answers = extract_student_answers(student_text)

print("\nModel Answers:", model_answers)
print("Student Answers:", student_answers)

total = min(len(model_answers), len(student_answers))

model_answers = model_answers[:total]
student_answers = student_answers[:total]

print("\nAligned Total Questions:", total)

score = 0

print("\n================ RESULT =================")

for i in range(total):
    if model_answers[i] == student_answers[i]:
        score += 1
        print(f"Q{i+1}: Correct ({model_answers[i]})")
    else:
        print(f"Q{i+1}: Wrong (M={model_answers[i]}, S={student_answers[i]})")

if total == 0:
    print("\nNo answers detected. OCR may have failed.")
    percentage = 0
else:
    percentage = (score / total) * 100

print("\n================ FINAL RESULT =================")
print("Score:", score)
print("Total:", total)
print("Percentage:", round(percentage, 2), "%")

os.makedirs("results", exist_ok=True)
file_path = "results/results.csv"

file_exists = os.path.isfile(file_path)

with open(file_path, "a", newline="") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow(["Student_ID", "Marks", "Total", "Percentage"])

    writer.writerow([student_name, score, total, round(percentage, 2)])

print("Result Saved")