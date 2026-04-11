import re
import csv
import os
import time
import sys

if len(sys.argv) > 1:
    student_name = sys.argv[1]
else:
    student_name = "student_1"

model_path = "processed/model/text/model.txt"
student_path = f"processed/students/{student_name}/text/student.txt"

while not (os.path.exists(model_path) and os.path.exists(student_path)):
    print("Waiting for OCR output...")
    time.sleep(1)

print("OCR files detected")

with open(model_path, "r") as f:
    model_text = f.read()

with open(student_path, "r") as f:
    student_text = f.read()

print("Files Loaded")

print("\nChecking extracted text...")
print("Model text length:", len(model_text))
print("Student text length:", len(student_text))

def remove_header(text):
    if "1." in text:
        return text.split("1.", 1)[1]
    return text

model_text = remove_header(model_text)
student_text = remove_header(student_text)

def clean_text(text):
    text = re.sub(r'([A-D])(\d+\.)', r'\1\n\2', text)
    text = re.sub(r'([A-D])Q\.', r'\1\nQ.', text)
    text = re.sub(r'(\d+)\.', r'\1. ', text)
    text = re.sub(r'(?<!\n)(\d+\.)', r'\n\1', text)
    return text

model_text = clean_text(model_text)
student_text = clean_text(student_text)

def extract_all_answers(text):
    text = text.upper()
    
    replacements = {
        "8": "B",
        "0": "D",
        "O": "D",
        "Q": "B",
        "P": "D"
    }
    
    for k, v in replacements.items():
        text = text.replace(k, v)
    
    answers = re.findall(r'ANSWER[:\s]*([A-D])', text)
    return answers

model_answers = extract_all_answers(model_text)
student_answers = extract_all_answers(student_text)

print("\nExtracted Answers")
print("Model Answers:", len(model_answers))
print("Student Answers:", len(student_answers))

total = min(len(model_answers), len(student_answers))
score = 0

print("\nResult")
for i in range(total):
    m = model_answers[i]
    s = student_answers[i]
    
    if m == s:
        score += 1
        print(f"Q{i+1}: Correct ({m})")
    else:
        print(f"Q{i+1}: Wrong (M={m}, S={s})")

percentage = (score / total) * 100 if total > 0 else 0

print("\nFinal Result")
print("Score:", score)
print("Total:", total)
print("Percentage:", round(percentage, 2), "%")

os.makedirs("results", exist_ok=True)
file_path = "results/results.csv"

with open(file_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Student_ID", "Marks", "Total", "Percentage"])
    writer.writerow([student_name, score, total, round(percentage, 2)])

print("Result Saved →", file_path)