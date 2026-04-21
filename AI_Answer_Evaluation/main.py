import json
from src.pdf_utils import pdf_to_images
from src.ocr import extract_text
from src.mcq_evaluation import extract_mcq_answers, evaluate_mcq

# -------------------------------
# FILE PATHS (YOUR ACTUAL FILES)
# -------------------------------
student_pdf = "/Users/nikhilbhanderi/Desktop/AI_Answer_Evaluation/data/student_answers/mcq_student_answer.pdf"
model_pdf = "/Users/nikhilbhanderi/Desktop/AI_Answer_Evaluation/data/model_answers/model_answer.pdf"

# -------------------------------
# STEP 1: Convert Student PDF → Images
# -------------------------------
student_images = pdf_to_images(student_pdf)

student_text = ""
for img in student_images:
    student_text += extract_text(img) + "\n"

# -------------------------------
# STEP 2: Convert Model PDF → Images
# -------------------------------
model_images = pdf_to_images(model_pdf)

model_text = ""
for img in model_images:
    model_text += extract_text(img) + "\n"

# 🔥 -------------------------------
# 🧠 STEP 3: DEBUG OCR OUTPUT (TEXT LEVEL)
# -------------------------------
print("\n--- STUDENT TEXT ---\n")
print(student_text)

print("\n--- MODEL TEXT ---\n")
print(model_text)

# -------------------------------
# STEP 4: Extract MCQ Answers
# -------------------------------
student_answers = extract_mcq_answers(student_text)
model_answers = extract_mcq_answers(model_text)

# 🔥 -------------------------------
# 🧪 STEP 5: DEBUG MCQ EXTRACTION (VERY IMPORTANT)
# -------------------------------
print("\n--- STUDENT MCQ ---\n")
print(student_answers)

print("\n--- MODEL MCQ ---\n")
print(model_answers)

# -------------------------------
# STEP 6: Evaluate
# -------------------------------
score, total = evaluate_mcq(student_answers, model_answers)

# -------------------------------
# STEP 7: Save Result
# -------------------------------
result = {
    "score": score,
    "total": total
}

with open("output/results/mcq_result.json", "w") as f:
    json.dump(result, f, indent=4)

# -------------------------------
# OUTPUT
# -------------------------------
print("\n✅ MCQ Evaluation Complete!")
print(f"Score: {score} / {total}")